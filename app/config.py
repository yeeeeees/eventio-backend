import os
import string
import random


class BaseConfig(object):
    """base config"""
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DB_URI', 'postgres://root:eventio@postgres/eventio')
    SECRET_KEY = os.environ.get("secret_key", ''.join(
        [random.choice(string.ascii_letters + string.digits) for n in range(16)]))


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
