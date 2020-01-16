import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_graphql_auth import GraphQLAuth
from app.config import TestingConfig, DevelopmentConfig, ProductionConfig


app = Flask(__name__)
app.config.from_object(DevelopmentConfig)

db = SQLAlchemy(app)

auth = GraphQLAuth(app)

from app.graphql.routes import api
from app.errors.handlers import errors

app.register_blueprint(api)
app.register_blueprint(errors)


def create_app():
    app = Flask(__name__)

    app.config.from_object(DevelopmentConfig if os.environ.get(
        "PRODUCTION", "false").lower() == 'true' else DevelopmentConfig)

    db.init_app(app)

    auth.init_app(app)

    from app.graphql.routes import api
    from app.errors.handlers import errors

    app.register_blueprint(api)
    app.register_blueprint(errors)

    return app
