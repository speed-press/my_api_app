""" Flask App Config """


class Config:
    """Base config."""
    SECRET_KEY = 'not victorias'
    STATIC_FOLDER = 'static'
    TEMPLATES_FOLDER = 'templates'

class ProdConfig(Config):
    FLASK_ENV = 'production'
    DEBUG = False
    TESTING = False
    DATABASE_URI = 'PROD_DB_URI'

class DevConfig(Config):
    FLASK_ENV = 'development'
    DEBUG = True
    TESTING = True
    DATABASE_URI = 'DEV_DATABASE_URI'

class TestConfig(Config):
    SERVER_NAME = 'localhost:5000'
    FLASK_ENV = 'development'
    DEBUG = True
    TESTING = True
    DATABASE_URI = 'DEV_DATABASE_URI'