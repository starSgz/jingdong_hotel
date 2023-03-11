# -*- coding: utf-8 -*-
"""
@Time ： 2023/3/8 22:28
@Auth ： star
@File ：User.py
"""
import json

from flask import Blueprint, render_template, request, jsonify, make_response

from jingdong_demo.config import redis_db
from jingdong_demo.models.model import UserModel
from jingdong_demo.utils.captchaImageService import operate_captcha
from jingdong_demo.utils.encryptService import operate_token
from jingdong_demo.utils.requestHeader import Auth

user = Blueprint('user', __name__)



@user.route('captchaImage',methods=['GET'])
def captchaImage():
    '''登录验证码'''
    try:
        # 生成验证码
        code = operate_captcha.generate_code()
        # 生成图片验证码
        image_base64_str = operate_captcha.generate_captcha_base64(code)

        # 生成唯一key
        code_key = operate_captcha.generate_code_key()

        # 存入Redis
        redis_db.set('verify_code:'+code_key, code.casefold(), 60 * 2)

        data = {
            "msg": "操作成功",
            "img": image_base64_str,
            "code": 200,
            "captchaEnabled": "true",
            "uuid": code_key,
        }

        return jsonify(data)
    except:
        data = {
            "msg": "操作失败",
            "code": 500,
            "captchaEnabled": "false",
        }
        return jsonify(data)

@user.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template('user/login.html')

    data = request.form
    username = data.get('username')
    password = data.get('password')

    # rsa = rsa_obj()
    # password = rsa.decrypt(password)

    # code = data.get('verify_code')
    # if data.get('uuid'):
    #     uuid = 'verify_code:' + data.get('uuid')
    # else:
    #     uuid = None
    #
    # code_ttl = redis_db.ttl(uuid)
    # # 验证码已经过期
    # if code_ttl <= 0:
    #     return jsonify({"code": 500, "msg": "验证码已经失效！"})
    #
    # # 获取redis中的code
    # redis_code = redis_db.get(uuid)
    #
    # # 验证码校验
    # if redis_code != code.casefold():
    #     return jsonify({"code": 500, "msg": "验证码错误！"})
    # else:
    #     redis_db.delete(uuid)

    query = UserModel.query.filter(UserModel.username == username).first()

    if query:
        if query.check_login_password(password):
            # 生成token
            layout_time = 60 * 60 * 24
            token = operate_token.create_token(query.id, query.username, layout_time)

            data = json.dumps({"userId":query.id})
            # 存储用户数据到redis中
            redis_db.set('jingdong_hotel:' + token , data , layout_time)

            #设置cookie
            # resp = make_response(render_template('user/test.html'))  # 设置响应体
            # resp.set_cookie("token", token, max_age=24 * 60 * 60)
            # return resp

            return render_template('user/test.html',token=token)
        return jsonify({"code": 500, "msg": "用户/密码错误！"})
    return jsonify({"code": 500, "msg": "登录用户：" + username + "不存在"})

@user.route('/logout',methods=['GET'])
def logout():
    '''注销'''
    try:
        #删除jwt
        auth_obj = Auth()
        if auth_obj.token:
            redis_db.delete("jingdong_hotel:{}".format(auth_obj.token))
            return jsonify({'code':200,'msg':'注销成功'})
        return jsonify({'code': 200, 'msg': '注销成功'})
    except:
        return jsonify({'code':500,'msg':'注销失败'})


@user.route('/test',methods=['GET','POST'])
def test():
    return render_template('user/test.html')


@user.route('/test1',methods=['GET','POST'])
def test1():
    return jsonify({"code":200})


@user.route('/')
def index():
    return render_template('user/login.html')