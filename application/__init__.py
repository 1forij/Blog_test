# app的初始化
# -*- coding: utf-8 -*-
from flask import Flask
from config import config

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app(config_name):
    '''程序的工厂函数'''
    app = Flask(__name__)
    app.config.from_object(config[config_name])


    # 初始化扩展
    db.init_app(app)

    # 注册蓝本
    from application.auth import auth_blue
    app.register_blueprint(auth_blue)

    from application.main import main_blue
    app.register_blueprint(main_blue)


    return app