#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import Flask
from jingdong_demo.views import register_blueprint
from .config import configDict
from .extensions import init_app


def create_app(configName='default'):
    app = Flask(__name__)
    register_blueprint(app)
    #调换数据库
    app.config.from_object(configDict.get(configName))
    init_app(app)
    return app
