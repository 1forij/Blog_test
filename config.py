# 配置
import os

basedir = os.path.abspath(os.path.dirname(__file__))

# 通用配置
class Config: 
    SECRET_KEY = '1214as'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # 邮件配置
    MAIL_SERVER = 'smtp.qq.com'
    MAIL_PROT = 465
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    MAIL_USERNAME = "329686980@qq.com"
    MAIL_PASSWORD = "hzxubbkivwilbghf"
    MAIL_DEFAULT_SENDER = "329686980@qq.com"

    @staticmethod # 使类不需要实例化就可以被调用
    def init_app(app):
        pass

# 开发模式
class Development(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')

# 生产模式
class Production(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data.sqlite')

config = {
    'development' : Development,
    'production' : Production,
}
