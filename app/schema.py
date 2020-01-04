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

    def mutate(self, info, username, fname, surname, email, password):
        user = UserModel.query.filter_by(username=username).first()

        if user is None:
            user = UserModel(username=username, fname=fname, surname=surname, email=email, password=password)
        else:
            return None

        db.session.add(user)
        db.session.commit()

        return CreateUser(user=user)


class CreateEvent(graphene.Mutation):
    class Arguments:
        title = graphene.String(required=True)
        description = graphene.String(required=True)
        uuid = graphene.Int(required=True)

    event = graphene.Field(lambda: Event)

    def mutate(self, info, title, description, uuid):
        organizer = UserModel.query.filter_by(uuid=uuid).first()
        event = EventModel(title=title, description=description)

        if organizer is not None:
            event.organizer = organizer
        else:
            return None

        db.session.add(event)
        db.session.commit()

        return CreateEvent(event=event)


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
        if uuid is not None:
            return query.filter(UserModel.uuid == uuid).first()
        else:
            return query.filter(UserModel.username == username).first()

    def resolve_event(self, info, **kwargs):
        query = Event.get_query(info)
        uuid = kwargs.get("uuid")
        title = kwargs.get('title')
        if uuid is not None:
            return query.filter(EventModel.uuid == uuid).first()
        else:
            return query.filter(EventModel.title == title).first()


class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()

    create_event = CreateEvent.Field()


schema = graphene.Schema(query=Query, mutation=Mutation, types=[User, Event])
