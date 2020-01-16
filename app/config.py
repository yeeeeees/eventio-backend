import os
import string
import random


class BaseConfig(object):
    """base config"""
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DB_URI', 'postgres://root:eventio@postgres/eventio')
    SECRET_KEY = "8e9cb88bf4ffb258e0c9446abcff43fe"
    JWT_SECRET_KEY = "saki"
    JWT_ACCESS_TOKEN_EXPIRES = False
    JWT_TOKEN_ARGUMENT_NAME = "Authorization"


class TestingConfig(BaseConfig):
    """testing config"""
    TESTING = True
    DEBUG = True


class DevelopmentConfig(BaseConfig):
    """dev config"""
    DEBUG = True


class ProductionConfig(BaseConfig):
    """production config"""
    TESTING = False
    DEBUG = False
