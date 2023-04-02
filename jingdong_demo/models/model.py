#!/usr/bin/python
# -*- coding: utf-8 -*-
from sqlalchemy import event, MetaData
from sqlalchemy_serializer import SerializerMixin

from .baseModel import BaseModel
from jingdong_demo.extensions import db
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash

UserQuestion = db.Table('user_question',
                       db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True, nullable=False),
                       db.Column('question_id', db.Integer, db.ForeignKey('question.id'), primary_key=True, nullable=False)
                       )


UserIp = db.Table('user_ip',
                       db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True, nullable=False),
                       db.Column('ip_id', db.Integer, db.ForeignKey('login.id'), primary_key=True, nullable=False)
                       )
# user 模型类
class UserModel(db.Model, BaseModel,SerializerMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)  # 自增ID
    username = db.Column(db.String(12), index=True, unique=True)  # 用户名
    password_hash = db.Column(db.String(512),nullable=False)  # 密码 密文
    sex = db.Column(db.String(2))  # 性别
    age = db.Column(db.SmallInteger, default=18)  # 年龄 默认18
    email = db.Column(db.String(50), unique=True)  # 邮箱
    icon = db.Column(db.String(70), default='default.png')  # 头像 默认为default.jpg
    lastLogin = db.Column(db.DateTime)  # 上次登录时间
    registerTime = db.Column(db.DateTime, default=datetime.utcnow)  # 注册时间
    confirm = db.Column(db.SmallInteger, default=False)  # 激活状态 默认未激活（需要发送邮件进行激活）

    user_question = db.relationship('QuestionModel', secondary=UserQuestion, backref=db.backref('user_question'))
    user_ip = db.relationship('LoginModel', secondary=UserIp, backref=db.backref('user_ip'))


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
        return "user object: name=%s" % self.username



class QuestionModel(db.Model, BaseModel,SerializerMixin):
    __tablename__ = 'question'
    id = db.Column(db.Integer, primary_key=True)  # 自增ID
    u_question = db.Column(db.String(250),nullable=False)
    answer = db.Column(db.String(250),nullable=False)


class LoginModel(db.Model, BaseModel, SerializerMixin):
    __tablename__ = 'login'
    id = db.Column(db.Integer, primary_key=True)  # 自增ID
    ip = db.Column(db.String(250), nullable=False, comment='登陆ip')
    login_time = db.Column(db.Integer, default=datetime.now, comment='登陆时间')
    logout_time = db.Column(db.Integer, comment='登出时间')

@event.listens_for(LoginModel, 'before_insert')
def set_logout_time(mapper, connection, target):
    target.logout_time = datetime.now() + timedelta(hours=6)

class JingDongModel(db.Model, BaseModel,SerializerMixin):
    __tablename__ = 'jingdong'
    sid = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(255),comment='地址')
    name = db.Column(db.String(255),comment='店名')
    cityName = db.Column(db.String(255),comment='城市')
    districtName = db.Column(db.String(255),comment='区域')
    brandName = db.Column(db.String(255),comment='品牌名称')
    totalComments = db.Column(db.String(255),comment='评论数')
    score = db.Column(db.String(1000),comment='评分')
    location = db.Column(db.String(255),comment='lat纬度，lon经度 ')
    price = db.Column(db.String(255),comment='价格')
    coverImageUrl = db.Column(db.String(255),comment='封面图片')
    amenities = db.Column(db.String(255),comment='设施')
    detailPage_url = db.Column(db.String(255),comment='详情页地址')
    grade = db.Column(db.String(255),comment='星级')
    checkInDate = db.Column(db.String(255),comment='入住时间')
    checkOutDate = db.Column(db.String(255),comment='离开时间')
    businessZoneName = db.Column(db.String(255),comment='商圈名称')
    province = db.Column(db.String(255),comment='省份')
    image_paths = db.Column(db.String(255),comment='图片路径')###

# python manage.py db init 初始化
# python manage.py db migrate 生成迁移文件
# python manage.py db upgrade 更新数据库