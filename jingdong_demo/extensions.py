#!/usr/bin/python
# -*- coding: utf-8 -*-

# from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# bootstrap = Bootstrap()
db = SQLAlchemy()
migrate = Migrate()


# 注册插件
def init_app(app):
    # 注册bootstrap插件
    # bootstrap.init_app(app)

    # 注册sqlalchemy
    db.init_app(app)

    # 注册migrate
    migrate.init_app(app=app, db=db)
