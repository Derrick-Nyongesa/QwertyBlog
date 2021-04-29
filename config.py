import os

class Config:
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://derrick:daniel@localhost/qwerty'

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SECRET_KEY = os.environ.get('SECRET_KEY')

    UPLOADED_PHOTOS_DEST ='app/static/photos'

class ProdConfig(Config):
    pass

class TestConfig(Config):
    pass

class DevConfig(Config):
    DEBUG = True


config_options = {
    'production':ProdConfig,
    'test':TestConfig,
    'development':DevConfig
}