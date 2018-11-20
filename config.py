#-*-coding:utf-8-*-
import os
basedir=os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY=os.environ.get('SECRET_KEY') or 'hard to guess string'
    SQLALCHEMY_POOL_SIZE = 2
    SQLALCHEMY_POOL_TIMEOUT = 30
    SQLALCHEMY_POOL_RECYCLE = -1

    MAIL_SERVER='smtp.126.com'
    MAIL_PORT='25'
    MAIL_USE_TLS=True
    MAIL_USERNAME=os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD=os.environ.get('MAIL_PASSWORD')
    FLASKY_MAIL_SUBJECT_PREFIX='[Flasky]'
    FLASKY_MAIL_SENDER='shygiant@126.com'

    # 追踪对象的修改并且发送信号
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    @staticmethod
    def init_app(app):
        pass

class DevelomentConfig(Config):
    DEBUG=True
    SQLALCHEMY_DATABASE_URI="mysql+pymysql://root:mnbvvbnm@192.168.1.101:3306/flasky_devdb?charset=utf8"


class TestingConfig(Config):
    TESTING=True
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:mnbvvbnm@192.168.1.101:3306/flasky_testdb?charset=utf8"

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:mnbvvbnm@192.168.1.101:3306/flasky_db?charset=utf8"

config={
    'development':DevelomentConfig,
    'testing':TestingConfig,
    'production':ProductionConfig,
    'default':DevelomentConfig
}