from flask import Blueprint, jsonify
from app import db
from app.models import *
from flask_graphql import GraphQLView
from app.schema import schema


api = Blueprint('api', __name__)


@api.route("/")
def home():
    user = User(name="saki")

    db.session.add(user)
    db.session.commit()
    return {"home": "page"}


# @api.route("/<string:variable>")
# def greeting(variable):
#    user = User.query.filter_by(name="saki").first()
#    return jsonify(name=str(user.name))


api.add_url_rule(
    "/graphiql",
    view_func=GraphQLView.as_view(
        'graphql',
        schema=schema,
        graphiql=True
    )
)
