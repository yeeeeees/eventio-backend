import graphene
from app import db
from graphene import relay
from flask import request, url_for
from app.utils import save_picture
from app.models import User as UserModel, Event as EventModel
from graphene_sqlalchemy import SQLAlchemyConnectionField, SQLAlchemyObjectType
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required, get_jwt_identity


EXT_IP = "http://34.89.206.63"


class User(SQLAlchemyObjectType):
    class Meta:
        model = UserModel
        interfaces = (relay.Node, )


class UserConnections(relay.Connection):
    class Meta:
        node = User


class Event(SQLAlchemyObjectType):
    class Meta:
        model = EventModel
        interfaces = (relay.Node, )


class EventConnections(relay.Connection):
    class Meta:
        node = Event


class CreateUser(graphene.Mutation):
    class Arguments:
        username = graphene.String(required=True)
        fname = graphene.String(required=True)
        surname = graphene.String(required=True)
        email = graphene.String(required=True)
        password = graphene.String(required=True)

    user = graphene.Field(User)
    message = graphene.String()
    success = graphene.Boolean()

    @classmethod
    def mutate(cls, root, info, username, fname, surname, email, password):
        user_with_same_username = UserModel.query.filter_by(username=username).first()
        user_with_same_email = UserModel.query.filter_by(email=email).first()
        image = request.files.get('profile_pic')

        args = {"username": username,
                "fname": fname,
                "surname": surname,
                "email": email,
                "password": password
                }

        if image:
            profile_picture = save_picture(image, "profile")
            args.update({"profile_pic": profile_picture})

        if user_with_same_username:
            return cls(user=None, message="That username is already taken. Plesae try again with different username.", success=False)

        if user_with_same_email:
            return cls(user=None, message="That email is already in use. Plesae try again with different email.", success=False)

        if not user_with_same_email and not user_with_same_username:
            user = UserModel(**args)

        db.session.add(user)
        db.session.commit()

        return cls(user=user, message="User created successfully.", success=True)


class EditUser(graphene.Mutation):
    class Arguments:
        uuid = graphene.Int(required=True)
        username = graphene.String(required=False)
        fname = graphene.String(required=False)
        surname = graphene.String(required=False)
        email = graphene.String(required=False)
        password = graphene.String(required=False)

    user = graphene.Field(User)
    message = graphene.String()
    success = graphene.Boolean()

    @classmethod
    @jwt_required
    def mutate(cls, root, info, uuid, username=None, fname=None, surname=None, email=None, password=None):
        user = UserModel.query.filter_by(uuid=uuid).first()

        user_with_same_username = UserModel.query.filter_by(username=username).first()
        user_with_same_email = UserModel.query.filter_by(email=email).first()
        image = request.files.get('profile_pic')

        args = {"username": username,
                "fname": fname,
                "surname": surname,
                "email": email,
                "password": password
                }

        if image:
            profile_picture = save_picture(image)
            args.update({"profile_pic": profile_picture})

        if user_with_same_username:
            return cls(user=None, message="That username is already taken. Please try again with different username.", success=False)

        if user_with_same_email:
            return cls(user=None, message="That email is already in use. Please try again with different email.", success=False)

        if not user:
            return cls(user=None, message="No user found with id. Please try again.", success=False)

        if not any(args.values()):
            return cls(user=None, message="Please supply some data to edit user with.", success=False)

        for key, value in args.items():
            if value is not None:
                setattr(user, key, value)

        db.session.commit()

        return cls(user=user, message="User edited successfully.", success=True)


class DeleteUser(graphene.Mutation):
    class Arguments:
        uuid = graphene.Int(required=True)

    message = graphene.String()
    success = graphene.Boolean()

    @classmethod
    @jwt_required
    def mutate(cls, root, info, uuid):
        user = UserModel.query.filter_by(uuid=uuid).first()

        if not user:
            return cls(message="No user found with that uuid. Please try again.", success=False)

        if len(user.created_events) > 0:
            for event in user.created_events:
                db.session.delete(event)

        db.session.delete(user)
        db.session.commit()

        return cls(message="User deleted successfully.", success=True)


class LoginUser(graphene.Mutation):
    class Arguments:
        username = graphene.String(required=False)
        email = graphene.String(required=False)
        password = graphene.String(required=True)

    message = graphene.String()
    success = graphene.Boolean()
    access_token = graphene.String()
    refresh_token = graphene.String()
    user = graphene.Field(User)

    @classmethod
    def mutate(cls, root, info, password, username=None, email=None):
        # TODO: add password decryption
        if not any([username, email]):
            return cls(message="Please enter your email/username to login.", success=False, access_token=None, refresh_token=None, user=None)
        if username:
            user = UserModel.query.filter_by(username=username).first()
        if email:
            user = UserModel.query.filter_by(email=email).first()

        if not user:
            return cls(message="Invalid username/email or password.", success=False, access_token=None, refresh_token=None, user=None)
        else:
            identity = {"uuid": user.uuid,
                        "username": user.username}

            return cls(message="Logged in succesfully.", success=True, access_token=create_access_token(identity=identity), refresh_token=create_refresh_token(identity=identity), user=user)


class CreateAccessToken(graphene.Mutation):

    access_token = graphene.String()
    success = graphene.Boolean()
    message = graphene.String()

    @classmethod
    @jwt_refresh_token_required
    def mutate(cls, root, info):
        identity = get_jwt_identity()
        user = UserModel.query.filter_by(uuid=identity.get("uuid")).first()

        if not user:
            return cls(message="Invalid JWT token submitted.", success=True, access_token=None)

        if not(user and user.username == identity.get("username")):
            return cls(message="Invalid JWT token submitted.", success=True, access_token=None)

        else:
            return cls(message="Access token created successfully.", success=True, access_token=create_access_token(identity=identity))


class CreateEvent(graphene.Mutation):
    class Arguments:
        title = graphene.String(required=True)
        description = graphene.String(required=True)
        organizer_uuid = graphene.Int(required=True)

    event = graphene.Field(Event)
    message = graphene.String()
    success = graphene.Boolean()

    @classmethod
    @jwt_required
    def mutate(cls, root, info, title, description, organizer_uuid):
        event = EventModel(title=title, description=description)
        organizer = UserModel.query.filter_by(uuid=organizer_uuid).first()
        image = request.files.get('event_thumbnail')

        if image:
            event_thumbnail = save_picture(image, "event")
            event.event_thumbnail = event_thumbnail

        if organizer:
            event.organizer = organizer

        else:
            return cls(event=None, message="Organizer not found. Please try again.", success=False)

        db.session.add(event)
        db.session.commit()

        return cls(event=event, message="Event created successfully.", success=True)


class JoinEvent(graphene.Mutation):
    class Arguments():
        user_uuid = graphene.Int(required=True)
        event_uuid = graphene.Int(required=True)

    event = graphene.Field(Event)
    user = graphene.Field(User)
    message = graphene.String()
    success = graphene.Boolean()

    @classmethod
    @jwt_required
    def mutate(cls, root, info, user_uuid, event_uuid):
        user = UserModel.query.filter_by(uuid=user_uuid).first()
        event = EventModel.query.filter_by(uuid=event_uuid).first()

        if not event:
            return cls(event=None, user=None, message="Event unavailable.", success=False)

        if not user:
            return cls(event=None, user=None, message="User not found.", success=False)

        if user is event.organizer:
            return cls(event=None, user=None, message="You can't join your own events.", success=False)

        if event in user.joined_events:
            return cls(event=None, user=None, message="User already joined.", success=False)

        if event not in user.joined_events:
            user.joined_events.append(event)

        db.session.commit()

        return cls(event=event, user=user, message="User joined successfully.", success=True)


class EditEvent(graphene.Mutation):
    class Arguments:
        uuid = graphene.Int(required=True)
        title = graphene.String(required=False)
        description = graphene.String(required=False)

    event = graphene.Field(Event)
    message = graphene.String()
    success = graphene.Boolean()

    @classmethod
    @jwt_required
    def mutate(cls, root, info, uuid, title=None, description=None):
        event = EventModel.query.filter_by(uuid=uuid).first()
        image = request.files.get('event_thumbnail')

        args = {"title": title,
                "description": description
                }

        if image:
            event_thumbnail = save_picture(image, "event")
            args.update({"eventio_thumbnail": event_thumbnail})

        else:
            return cls(event=None, message="Please supply an event thumbnail picture.", success=False)

        if not event:
            return cls(event=None, message="No event found with that uuid. Please try again.", success=False)

        if not any(args.values()):
            return cls(event=None, message="Please supply some data to edit event with.", success=False)

        for key, value in args.items():
            if value is not None:
                setattr(event, key, value)

        db.session.commit()

        return cls(event=event, message="Event edited sucessfully.", success=True)


class LeaveEvent(graphene.Mutation):
    class Arguments():
        user_uuid = graphene.Int(required=True)
        event_uuid = graphene.Int(required=True)

    event = graphene.Field(Event)
    user = graphene.Field(User)
    message = graphene.String()
    success = graphene.Boolean()

    @classmethod
    @jwt_required
    def mutate(cls, root, info, user_uuid, event_uuid):
        user = UserModel.query.filter_by(uuid=user_uuid).first()
        event = EventModel.query.filter_by(uuid=event_uuid).first()

        if not event:
            return cls(event=None, user=None, message="Event unavailable.", success=False)

        if not user:
            return cls(event=None, user=None, message="User not found.", success=False)

        if user is event.organizer:
            return cls(event=None, user=None, message="You can't leave your own events.", success=False)

        if event not in user.joined_events:
            return cls(event=None, user=None, message="Can't find an event to leave. Please try again.", success=False)

        if event in user.joined_events:
            user.joined_events.remove(event)

        db.session.commit()

        return cls(event=event, user=user, message="Left event successfully.", success=True)


class DeleteEvent(graphene.Mutation):
    class Arguments:
        uuid = graphene.Int(required=True)

    message = graphene.String()
    success = graphene.Boolean()

    @classmethod
    @jwt_required
    def mutate(cls, root, info, uuid):
        event = EventModel.query.filter_by(uuid=uuid).first()

        if not event:
            return cls(message="No event found with that uuid. Please try again.", success=False)

        db.session.delete(event)
        db.session.commit()

        return cls(message="The event was deleted successfully", success=True)


class Query(graphene.ObjectType):
    node = relay.Node.Field()

    # queries that return individual models
    user = graphene.Field(User, uuid=graphene.Int(), username=graphene.String())

    event = graphene.Field(Event, uuid=graphene.Int(), title=graphene.String())

    # queries that return all models of given type
    all_users = SQLAlchemyConnectionField(UserConnections)

    all_events = SQLAlchemyConnectionField(EventConnections)

    # resolvers
    def resolve_user(self, info, **kwargs):
        query = User.get_query(info)
        uuid = kwargs.get("uuid", None)
        username = kwargs.get('username')
        if uuid:
            return query.filter(UserModel.uuid == uuid).first()
        else:
            return query.filter(UserModel.username == username).first()

    def resolve_event(self, info, **kwargs):
        query = Event.get_query(info)
        uuid = kwargs.get("uuid", None)
        title = kwargs.get('title')
        if uuid:
            return query.filter(EventModel.uuid == uuid).first()
        else:
            return query.filter(EventModel.title == title).first()


class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()
    login_user = LoginUser.Field()
    edit_user = EditUser.Field()
    delete_user = DeleteUser.Field()

    get_access_token = CreateAccessToken.Field()

    create_event = CreateEvent.Field()
    edit_event = EditEvent.Field()
    join_event = JoinEvent.Field()
    leave_event = LeaveEvent.Field()
    delete_event = DeleteEvent.Field()


schema = graphene.Schema(query=Query, mutation=Mutation, types=[User, Event])
