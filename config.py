import os

class Config:
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://derrick:daniel@localhost/qwerty'

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