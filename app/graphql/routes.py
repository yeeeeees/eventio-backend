from flask import Blueprint, jsonify
from app import db
from app.models import *
from flask_graphql import GraphQLView
from app.schema import schema


api = Blueprint('api', __name__)


@api.route("/")
def home():
    user = User(username="saki2", fname="saki", surname="saki", email="saki@saki.hr", password="saki")
    db.session.add(user)
    event = Event(title="idk", description="i don't know", organizer=User.query.filter_by(username="saki2").first())
    db.session.add(event)
    db.session.commit()
    return {"home": "page"}


# route for graphiql
api.add_url_rule(
    "/graphiql",
    "graphiql",
    view_func=GraphQLView.as_view(
        'graphql',
        schema=schema,
        graphiql=True
    )
)

# route for graphql without user interface (POST request)
api.add_url_rule(
    "/graphql",
    "graphql",
    view_func=GraphQLView.as_view(
        'graphql',
        schema=schema,
        batch=True
    )
)
