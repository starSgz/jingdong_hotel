#!/usr/bin/python
# -*- coding: utf-8 -*-
from flask_migrate import MigrateCommand
from flask_script import Manager,Server
from jingdong_demo import create_app
from flask import request, render_template
# 创建app
from jingdong_demo.config import redis_db
from jingdong_demo.utils.requestHeader import Auth

app = create_app()

# flask-script命令行管理插件
manager = Manager(app=app)
manager.add_command('db',MigrateCommand)
#设置配置
manager.add_command("runserver", Server(
    host = '127.0.0.1',port=5000,use_debugger=True)
)

required_list = ['/login','/captchaImage','/static/css/style_1.css','/static/js/bootstrap.min.js',
                 '/static/js/jquery.min.js','/static/js/common.js','/data:image/jpg;base64,',
                 '/static/js/map.js',
                 '/static/js/js.js','/static/css/style.css','/static/js/china.js','/static/js/echarts.min.js','/static/font/DS-DIGIT.TTF',
                 '/bigScreen','/map','/brandTop','/grade','/radar','/brandAvgPrice']


# @app.before_request
# def before_request():
#     print(request.path)
#     if request.path not in required_list:
#         auth = Auth()
#         if auth.token:
#             token_redis = 'jingdong_hotel:'+auth.token
#             time_ttl = redis_db.ttl(token_redis)
#             if time_ttl <= 0:
#                 return render_template('user/login.html')
#
#         else:
#             return render_template('user/login.html')
#

if __name__ == '__main__':
    manager.run()
