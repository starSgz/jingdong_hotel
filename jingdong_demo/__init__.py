#!/usr/bin/python
# -*- coding: utf-8 -*-
import os

from flask import Flask
from jingdong_demo.views import register_blueprint
from .config import configDict
from .extensions import init_app
from mychche import cache

def create_app(configName='default'):
    app = Flask(__name__)
    cache_dir = os.path.join(app.root_path, 'cache')  # 获取当前项目目录下的 cache 文件夹路径
    if not os.path.exists(cache_dir):  # 如果 cache 文件夹不存在，则创建它
        os.makedirs(cache_dir)
    cache.init_app(app=app, config={'CACHE_TYPE':'filesystem','CACHE_DIR': cache_dir,'CACHE_DEFAULT_TIMEOUT':31622400}) #存到本地，重新运行缓冲也在
    # cache.init_app(app=app, config={'CACHE_TYPE':'simple'}) #存在内存，重新运行之后缓冲失效
    register_blueprint(app)
    #调换数据库
    app.config.from_object(configDict.get(configName))
    init_app(app)
    return app


