#!/usr/bin/python
# -*- coding: utf-8 -*-
from flask_migrate import MigrateCommand
from flask_script import Manager,Server
from jingdong_demo import create_app

# 创建app
app = create_app()

# flask-script命令行管理插件
manager = Manager(app=app)
manager.add_command('db',MigrateCommand)
#设置配置
manager.add_command("runserver", Server(
    host = '0.0.0.0',port=5000,use_debugger=True)
)

if __name__ == '__main__':
    manager.run()
