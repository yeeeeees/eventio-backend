import graphene
from app import db
from graphene import relay
from app.models import User as UserModel, Event as EventModel
from graphene_sqlalchemy import SQLAlchemyConnectionField, SQLAlchemyObjectType


class User(SQLAlchemyObjectType):
    class Meta:
        model = UserModel
        interfaces = (relay.Node, )


class UserConnection(relay.Connection):
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

    user = graphene.Field(lambda: User)
    message = graphene.String()

    def mutate(self, info, username, fname, surname, email, password):
        user_with_same_username = UserModel.query.filter_by(username=username).first()
        user_with_same_email = UserModel.query.filter_by(email=email).first()

        if user_with_same_username:
            return CreateUser(user=None, message="That username is already taken. Plesae try again with different email.")

        if user_with_same_email:
            return CreateUser(user=None, message="That email is already in use. Plesae try again with different email.")

        if not user_with_same_email and not user_with_same_username:
            user = UserModel(username=username, fname=fname, surname=surname, email=email, password=password)

        db.session.add(user)
        db.session.commit()

        return CreateUser(user=user, message="User created successfully.")


class EditUser(graphene.Mutation):
    class Arguments:
        uuid = graphene.Int(required=True)
        username = graphene.String(required=False)
        fname = graphene.String(required=False)
        surname = graphene.String(required=False)
        email = graphene.String(required=False)
        password = graphene.String(required=False)

    user = graphene.Field(lambda: User)
    message = graphene.String()

    def mutate(self, info, uuid, username=None, fname=None, surname=None, email=None, password=None):
        user = UserModel.query.filter_by(uuid=uuid).first()

        user_with_same_username = UserModel.query.filter_by(username=username).first()
        user_with_same_email = UserModel.query.filter_by(email=email).first()

        args = {"username": username,
                "fname": fname,
                "surname": surname,
                "email": email,
                "password": password
                }

        if user_with_same_username:
            return EditUser(user=None, message="That username is already taken. Please try again with different username.")

        if user_with_same_email:
            return EditUser(user=None, message="That email is already in use. Please try again with different email.")

        if not user:
            return EditUser(user=None, message="No user found with id. Please try again.")

        if not any(args.values()):
            return EditUser(user=None, message="Please supply some data to edit user with.")

        for key, value in args.items():
            if value is not None:
                setattr(user, key, value)

        db.session.commit()

        return EditUser(user=user, message="User edited successfully.")


class DeleteUser(graphene.Mutation):
    class Arguments:
        uuid = graphene.Int(required=True)

    message = graphene.String()

    def mutate(self, info, uuid):
        user = UserModel.query.filter_by(uuid=uuid).first()

        if not user:
            return DeleteUser(message="No user found with that uuid. Please try again.")

        db.session.delete(user)
        db.session.commit()

        return DeleteUser(message="User deleted successfully.")


class CreateEvent(graphene.Mutation):
    class Arguments:
        title = graphene.String(required=True)
        description = graphene.String(required=True)
        organizer_uuid = graphene.Int(required=True)

    event = graphene.Field(lambda: Event)
    message = graphene.String()

    def mutate(self, info, title, description, organizer_uuid):
        organizer = UserModel.query.filter_by(uuid=organizer_uuid).first()
        event = EventModel(title=title, description=description)

        if not organizer:
            event.organizer = organizer

        else:
            return CreateEvent(event=None, message="Organizer not found. Please try again.")

        db.session.add(event)
        db.session.commit()

        return CreateEvent(event=event, message="Event created successfully.")


class EditEvent(graphene.Mutation):
    class Arguments:
        uuid = graphene.Int(required=True)
        title = graphene.String(required=False)
        description = graphene.String(required=False)

    event = graphene.Field(lambda: Event)
    message = graphene.String()

    def mutate(self, info, uuid, title=None, description=None):
        event = EventModel.query.filter_by(uuid=uuid).first()

        args = {"title": title,
                "description": description
                }

        if not event:
            return EditEvent(event=None, message="No event found with that uuid. Please try again.")

        if not any(args.values()):
            return EditEvent(event=None, message="Please supply some data to edit event with.")

        for key, value in args.items():
            if value is not None:
                setattr(event, key, value)

        db.session.commit()

        return EditEvent(event=event, message="Event edited sucessfully.")


class DeleteEvent(graphene.Mutation):
    class Arguments:
        uuid = graphene.Int(required=True)

    message = graphene.String()

    def mutate(self, info, uuid):
        event = EventModel.query.filter_by(uuid=uuid).first()

        if not event:
            return DeleteEvent(message="No event foud with that uuid. Please try again.")

        db.session.delete(event)
        db.session.commit()

        return DeleteEvent(message="The event was deleted successfully")


class Query(graphene.ObjectType):
    node = relay.Node.Field()

    # queries that return individual models
    user = graphene.Field(lambda: User, uuid=graphene.Int(), username=graphene.String())

    event = graphene.Field(lambda: Event, uuid=graphene.Int(), title=graphene.String())

    # queries that return all models of given type
    all_users = SQLAlchemyConnectionField(UserConnection)

    all_events = SQLAlchemyConnectionField(EventConnections)

    # resolvers
    def resolve_user(self, info, **kwargs):
        query = User.get_query(info)
        uuid = kwargs.get("uuid")
        username = kwargs.get('username')
        if not uuid:
            return query.filter(UserModel.uuid == uuid).first()
        else:
            return query.filter(UserModel.username == username).first()

    def resolve_event(self, info, **kwargs):
        query = Event.get_query(info)
        uuid = kwargs.get("uuid")
        title = kwargs.get('title')
        if not uuid:
            return query.filter(EventModel.uuid == uuid).first()
        else:
            return query.filter(EventModel.title == title).first()


class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()
    edit_user = EditUser.Field()
    delete_user = DeleteUser.Field()

    create_event = CreateEvent.Field()
    edit_event = EditEvent.Field()
    delete_event = DeleteEvent.Field()


schema = graphene.Schema(query=Query, mutation=Mutation, types=[User, Event])
