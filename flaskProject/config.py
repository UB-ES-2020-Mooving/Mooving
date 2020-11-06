from decouple import config
class Config(object):
    pass

class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = config('DATABASE_URL', default='localhost')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    STATIC_FOLDER = "../frontend/dist/static"
    TEMPLATE_FOLDER = "../frontend/dist"
    SECRET_KEY = config('SECRET_KEY', default='localhost')

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///data.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    STATIC_FOLDER = "../frontend/dist/static"
    TEMPLATE_FOLDER = "../frontend/dist"
    SECRET_KEY = "kdsfklsmfakfmafmadslvsdfasdf"

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig
}

