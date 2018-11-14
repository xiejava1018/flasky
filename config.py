#-*-coding:utf-8-*-
import os
basedir=os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY=os.environ.get('SECRET_KEY') or 'hard to guess string'

    @staticmethod
    def init_app(app):
        pass

class DevelomentConfig(Config):
    DEBUG=True
    SQLALCHEMY_DATABASE_URI='"mysql+pymysql://root:mnbvvbnm@192.168.1.101:3306/test?charset=utf8"'

class TestingConfig(Config):
    TESTING=True
    SQLALCHEMY_DATABASE_URI = '"mysql+pymysql://root:mnbvvbnm@192.168.1.101:3306/test?charset=utf8"'

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = '"mysql+pymysql://root:mnbvvbnm@192.168.1.101:3306/test?charset=utf8"'

config={
    'development':DevelomentConfig,
    'testing':TestingConfig,
    'production':ProductionConfig,
    'default':DevelomentConfig
}