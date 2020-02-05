from flask import Blueprint, jsonify
from app import db
from app.models import *
# from flask_graphql import GraphQLView
from graphene_file_upload.flask import FileUploadGraphQLView
from app.schema import schema


api = Blueprint('api', __name__)


# route for graphiql
api.add_url_rule(
    "/graphiql",
    "graphiql",
    view_func=FileUploadGraphQLView.as_view(
        'graphql',
        schema=schema,
        graphiql=True,
        context={'session': db.session}
    )
)

# route for graphql without user interface (POST request)
api.add_url_rule(
    "/graphql",
    "graphql",
    view_func=FileUploadGraphQLView.as_view(
        'graphql',
        schema=schema,
        batch=True,
        context={'session': db.session}
    )
)
