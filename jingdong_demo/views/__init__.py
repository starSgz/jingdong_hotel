#!/usr/bin/python
# -*- coding: utf-8 -*-
from .Charts import charts
from .User import user

#添加蓝图
blueprint_config = [
    (user, ''),
    (charts, ''),
]


# 蓝图注册
def register_blueprint(app):
    for blueprintName, prefix in blueprint_config:
        app.register_blueprint(blueprintName, url_prefix=prefix)

