import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyConnectionField, SQLAlchemyObjectType
from app.models import User as UserModel, Event as EventModel


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


class Query(graphene.ObjectType):
    node = relay.Node.Field()

    all_users = SQLAlchemyConnectionField(UserConnection)

    all_events = SQLAlchemyConnectionField(EventConnections)


schema = graphene.Schema(query=Query, types=[User, Event])
