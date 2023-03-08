#!/usr/bin/python
# -*- coding: utf-8 -*-

from .main import main
from .User import user

#添加蓝图
blueprint_config = [
    (main, ''),
    (user, ''),
]


# 蓝图注册
def register_blueprint(app):
    for blueprintName, prefix in blueprint_config:
        app.register_blueprint(blueprintName, url_prefix=prefix)

