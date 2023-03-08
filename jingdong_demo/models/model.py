#!/usr/bin/python
# -*- coding: utf-8 -*-
from .baseModel import BaseModel
from jingdong_demo.extensions import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash


# user 模型类
class UserModel(db.Model, BaseModel):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)  # 自增ID
    username = db.Column(db.String(12), index=True, unique=True)  # 用户名
    password_hash = db.Column(db.String(128),nullable=False)  # 密码 密文
    sex = db.Column(db.Boolean, default=True)  # 性别
    age = db.Column(db.SmallInteger, default=18)  # 年龄 默认18
    email = db.Column(db.String(50), unique=True)  # 邮箱
    icon = db.Column(db.String(70), default='default.png')  # 头像 默认为default.jpg
    lastLogin = db.Column(db.DateTime)  # 上次登录时间
    registerTime = db.Column(db.DateTime, default=datetime.utcnow)  # 注册时间
    confirm = db.Column(db.SmallInteger, default=False)  # 激活状态 默认未激活（需要发送邮件进行激活）

    # 明文密码（只读）
    @property
    def password(self):
        raise AttributeError(u'文明密码不可读')

    # 写入密码，同时计算hash值，保存到模型中
    @password.setter
    def password(self, value):
        self.password_hash = generate_password_hash(value)

    # 检查密码是否正确
    def check_login_password(self, password):
        return check_password_hash(self.password_hash, password)

    # 显示对象中的信息
    def __repr__(self):
        return "user object: name=%s" % self.user_name


# python manage.py db init 初始化
# python manage.py db migrate 生成迁移文件
# python manage.py db upgrade 更新数据库