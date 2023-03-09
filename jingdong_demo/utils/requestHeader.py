import json
from datetime import datetime
from flask import request
from flask_restful import fields

from jingdong_demo.config import redis_db


class DateEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime("%Y-%m-%d %H:%M:%S")
        else:
            return json.JSONEncoder.default(self, obj)


class CustomDate(fields.DateTime):
    '''
    自定义CustomDate,原有的fileds.DateTime序列化后
    只支持 rfc822,ios8601 格式，新增 strftime 格式
    strftime格式下支持 format 参数，默认为 '%Y-%m-%d %H:%M:%S'
    '''

    def __init__(self, dt_format='rfc822', format=None, **kwargs):
        super().__init__(**kwargs)
        self.dt_format = dt_format

    def format(self, value):
        if self.dt_format in ('rfc822', 'iso8601'):
            return super().format(value)
        elif self.dt_format == 'strftime':
            if isinstance(value, str):
                return value
            return value.strftime('%Y-%m-%d %H:%M:%S')

        else:
            raise Exception('Unsupported date format %s' % self.dt_format)

class Auth(object):
    '''处理请求头'''
    def __init__(self):
        self.token=None
        auth = request.headers.get('Authorization')
        if auth  and auth.startswith('Bearer '):
            self.token = auth[7:]

    def get_Auth_redis(self):
        if not self.token:
            return None
        return redis_db.get("xwhz_device:"+self.token)




