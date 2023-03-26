#!/usr/bin/python
# -*- coding: utf-8 -*-

import os

import redis

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = '123456'

    # 是否追踪数据库中数据的改变
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    BOOTSTRAP_SERVE_LOCAL = True
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True


class DevConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:123456@127.0.0.1:3306/jingdong_hotel'
    # SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://{}:{}@{}:{}/{}?charset=utf8'.format('root','123456','127.0.0.1','3306','jingdong_hotel')
    DEBUG = True
    TESTING = False


# class TestConfig(Config):
#     SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:102487aa@127.0.0.1:3306/jingdong_demo'
#     DEBUG = False
#     TESTING = True
#
#
# class ProductConfig(Config):
#     SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:102487aa@127.0.0.1:3306/jingdong_demo'
#     DEBUG = False
#     TESTING = False


configDict = {
    'default': DevConfig,
    'dev': DevConfig,
    # 'test': TestConfig,
    # 'production': ProductConfig,
}


#配置redis
class RedisConf:
    # 配置基本参数
    pwd = ""
    host = "127.0.0.1"
    port = 6379
class RedisDB:
    # 初始化redis
    def __init__(self):
        # 设置主机、端口号和密码
        redis_pool = redis.ConnectionPool(host=redis_conf.host, port=redis_conf.port, password=redis_conf.pwd, decode_responses=True)
        self.__strict_redis = redis.StrictRedis(connection_pool=redis_pool)

    # 在redis中添加键值，并设置过期时间
    def set(self, key, value, expiry):
        self.__strict_redis.set(name=key, value=value, ex=expiry)

    # 在redis中添加键值，不设置过期时间
    def set_forerver(self, key, value):
        self.__strict_redis.set(name=key, value=value)

    # 获取值
    def get(self, key):
        return self.__strict_redis.get(name=key)

    # 获取键值的剩余时间
    def ttl(self, key):
        # Time To Live
        return self.__strict_redis.ttl(name=key)

    #删除键值
    def delete(self,key):
        return  self.__strict_redis.delete(key)
redis_conf = RedisConf()
# 设置单例模式
redis_db = RedisDB()