# -*- coding: utf-8 -*-
"""
@Time ： 2023/3/8 22:28
@Auth ： star
@File ：User.py
"""
import json
import calendar
from datetime import timedelta,datetime,time
from urllib.parse import parse_qs

from sqlalchemy import func, distinct
from flask import Blueprint, render_template, request, jsonify, make_response

from jingdong_demo.config import redis_db
from jingdong_demo.extensions import db
from jingdong_demo.models.model import UserModel, QuestionModel, LoginModel, JingDongModel
from jingdong_demo.utils.captchaImageService import operate_captcha
from jingdong_demo.utils.encryptService import operate_token
from jingdong_demo.utils.requestHeader import Auth

import pandas as pd
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
        return render_template('admin/login.html')

    data = request.form
    username = data.get('username')
    password = data.get('password')

    # rsa = rsa_obj()
    # password = rsa.decrypt(password)

    code = data.get('captcha')
    if data.get('uuid'):
        uuid = 'verify_code:' + data.get('uuid')
    else:
        uuid = None
    code_ttl = redis_db.ttl(uuid)
    # 验证码已经过期
    if code_ttl <= 0:
        return jsonify({"code": 500, "msg": "验证码已经失效！"})
    # 获取redis中的code
    redis_code = redis_db.get(uuid)

    # 验证码校验
    if redis_code != code.casefold():
        return jsonify({"code": 500, "msg": "验证码错误！"})
    else:
        redis_db.delete(uuid)

    query = UserModel.query.filter(UserModel.username == username).first()

    if query:
        if query.check_login_password(password):
            # 生成token
            layout_time = 60 * 60 * 24
            token = operate_token.create_token(query.id, query.username, layout_time)

            data = json.dumps({"userId":query.id})
            # 存储用户数据到redis中
            redis_db.set('jingdong_hotel:' + token , data , layout_time)
            print((datetime.now() + timedelta(hours=6)))
            setL = LoginModel(ip=request.remote_addr,login_time=datetime.now() , logout_time=(datetime.now() + timedelta(hours=6)))
            db.session.add(setL)
            query.user_ip.append(setL)
            return jsonify({"code":200,"token":token,"msg":"登陆成功！"})
        return jsonify({"code": 500, "msg": "用户/密码错误！"})
    return jsonify({"code": 500, "msg": "登录用户：" + username + "不存在"})


# /forgetPwd
@user.route('/forgetPwd',methods=['GET','POST'])
def forgetPwd():
    if request.method == 'GET':
        return render_template("admin/forgetPwd.html",data={"code":200,"msg":"跳转成功！"})
    data = request.form
    print(data)
    username = data.get('username')

    # code = data.get('captcha')
    # if data.get('captcha'):
    #     uuid = 'verify_code:' + data.get('captcha')
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
        return render_template('admin/forgetPwdAnswer.html',data={"code":200,"msg":"账户存在！","result":[{"question":i.u_question,"id":i.id} for i in query.user_question],"uid":query.id})
    return render_template('admin/forgetPwd.html',data={"code":500,"msg":"账户不存在！"})

@user.route('/register',methods=['GET','POST'])
def register():
    if request.method == 'GET':
        return render_template('admin/register.html')
    args = request.form.to_dict()
    query = UserModel.query.filter(UserModel.username==args.get("username")).first()
    if query:
        return jsonify({"code":500,"msg":"用户已存在"})
    query_email = UserModel.query.filter(UserModel.email == args.get("email")).first()
    if query_email:
        return jsonify({"code": 500, "msg": "邮箱已存在"})

    arg_filter={}
    for k,v in args.items():
        if k == 'password' and v=='':
            return jsonify({"code":500,"msg":"密码不允许为空"})
        if k!="question_1" and k!="question_2" and k!='answer_2' and k!='answer_1':
            arg_filter[k]=v
        if k=="question_1" or k=="question_2" or k=='answer_2' or k=='answer_1' or k=='email':
            if v=='':
                return jsonify({"code":500,"msg":"问题/答案不允许为空"})

    addUser = UserModel(**arg_filter)
    db.session.add(addUser)
    questions = []
    for i in range(1, 3):
        question_text = request.form[f'question_{i}']
        answer_text = request.form[f'answer_{i}']
        question = QuestionModel(u_question=question_text, answer=answer_text)
        questions.append(question)
    addUser.user_question.extend(questions)
    return jsonify({"code": 200, "msg": "注册成功"})

@user.route('/forgetPwdAnswer',methods=['GET','POST'])
def forgetPwdAnswer():#forgetPwdAnswer
    if request.method == 'GET':
        return render_template('admin/forgetPwdAnswer.html')
    result = request.get_json()
    if len(result)<2:
        return jsonify({"code": 500, "msg": "密保问题错误"})
    for i in result:
        query = QuestionModel.query.filter(QuestionModel.id==i['id']).first()
        print(query)
        if query.answer != i['answer']:
            print(query.answer,i['answer'])
            return jsonify({"code": 500, "msg": "密保问题错误"})
        return jsonify({"code": 200, "msg": "校验成功","token":"id"})

@user.route('/resetPwd/<uid>',methods=['GET','POST'])
def resetPwd(uid):#forgetPwdAnswer
    if request.method == 'GET':
        return render_template('admin/resetPwd.html',data={"uid":uid})
    data = request.data.decode('utf-8')
    form_data = parse_qs(data)
    print(form_data)
    resetPwd_1 = form_data.get('resetPwd_1')[0]
    resetPwd_2 = form_data.get('resetPwd_2')[0]
    print(resetPwd_1,resetPwd_1)
    if resetPwd_1!=resetPwd_2:
        return jsonify({"code": 500, "msg": "密码不一致"})
    uid =  form_data.get('uid')[0]
    query = UserModel.query.filter(UserModel.id == uid).first()
    # print(query.password)
    print(query)
    query.password=resetPwd_1
    return jsonify({"code": 200, "msg": "修改成功"})


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



@user.route('/',methods=['GET'])
def index():
    return render_template('index/index.html')

@user.route('/polish',methods=['GET','POST'])
def polish():
    if request.method=='GET':
        query = UserModel.query.filter(UserModel.id==4).first()
        dic = query.to_dict(rules=('-user_ip','-password_hash','-user_question'))
        q_n_list = query.user_question
        q_a=[]
        for i in q_n_list:
            q_a.append({"id":i.id,"question":i.u_question,"answer":i.answer})
        dic['q_a']=q_a
        return render_template('admin/polish.html',data=dic)
    args = request.form
    print(args)
    query = UserModel.query.filter(UserModel.id == 4).first()
    password = args.get('password')
    age = args.get('age')
    email = args.get('email')
    sex =  args.get('sex')
    answer_1 = args.get('answer_1')
    answer_2 = args.get('answer_2')
    if password:
        query.password = password
    if age:
        print(7777)
        query.age = age
    query.email = email
    query.sex = sex
    query.user_question[0].answer = answer_1
    query.user_question[1].answer = answer_2

    query = UserModel.query.filter(UserModel.id == 4).first()
    dic = query.to_dict(rules=('-user_ip', '-password_hash', '-user_question'))
    q_n_list = query.user_question
    q_a = []
    for i in q_n_list:
        q_a.append({"id": i.id, "question": i.u_question, "answer": i.answer})
    dic['q_a'] = q_a
    print(dic)
    return jsonify({
        'code':200
    })

def get_data(start_time, end_time):

    res_ = UserModel.query.filter(UserModel.id==1).filter(LoginModel.login_time >= start_time, LoginModel.login_time <= end_time).first()
    if res_:
        query = res_.user_ip
    else:
        query=[]
    ip_count = db.session.query(distinct(LoginModel.ip)).count()
    # 账户登录次数
    login_count = len(query)
    # 在线时长时间
    # print(start_time,end_time)
    # print(type(start_time),end_time) #datetime类型
    online_time = db.session.query(func.sum(LoginModel.logout_time - LoginModel.login_time)).filter(LoginModel.login_time >= start_time, LoginModel.login_time <= end_time).scalar()#秒
    if online_time==None:
        online_time=0
    online_time_ = timedelta(seconds=int(online_time)) if online_time else timedelta(seconds=0)
    # # 平均操作时长
    avg_operation_time = (online_time_ / login_count).total_seconds() if online_time_ and login_count else 0
    print(ip_count, login_count, online_time, avg_operation_time)

    return {
        "ip_count": ip_count,
        "login_count": login_count,
        "online_time": int(online_time),
        "avg_operation_time": avg_operation_time
    }


@user.route('/welcome',methods=['GET'])
def welcome():
    #查询当前用户
    res_ = UserModel.query.filter(UserModel.id==4).first()
    query = res_.user_ip
    data = {}
    data['total']=len(query)
    res = [[q.id, q.ip, q.login_time, q.logout_time] for q in query]
    df = pd.DataFrame(res, columns=['id', 'ip', 'login_time', 'logout_time'])

    #不同ip数目
    ip_count = df.groupby('ip').count().reset_index()
    ip_count = ip_count[['ip', 'id']]
    ip_count.columns = ['ip', 'count']
    data['ipLogin'] = int(len(ip_count))

    # 按照登录时间排序，并选择最后一条记录
    last_login = df.sort_values('login_time').tail(1)
    ip = last_login['ip'].iloc[0]
    last_login_time = last_login['login_time'].iloc[0]
    data['last_ip'] = ip
    data['last_login_time'] = str(last_login_time)

    # 统计总计数据
    total_data = get_data(datetime(1970, 1, 1), datetime.now())
    data['total_data'] = total_data

    # 统计今日数据
    today = datetime.now().date()
    today_start = datetime.combine(today, time.min)
    today_end = datetime.combine(today, time.max)
    today_data = get_data(today_start, today_end)
    data['today_data'] = today_data

    # 统计昨日数据
    yesterday = datetime.now().date() - timedelta(days=1)
    yesterday_start = datetime.combine(yesterday, time.min)
    yesterday_end = datetime.combine(yesterday, time.max)
    yesterday_data = get_data(yesterday_start, yesterday_end)
    data['yesterday_data'] = yesterday_data

    # 统计本周数据
    this_week_start = datetime.now().date() - timedelta(days=datetime.now().weekday())
    this_week_end = datetime.now().date() + timedelta(days=6-datetime.now().weekday())
    this_week_start = datetime.combine(this_week_start, time.min)
    this_week_end = datetime.combine(this_week_end, time.max)
    this_week_data = get_data(this_week_start, this_week_end)
    data['this_week_data'] = this_week_data

    # 统计本月数据
    this_month_start = datetime.now().replace(day=1).date()
    print(this_month_start)
    this_month_end = datetime.now().replace(day=calendar.monthrange(datetime.now().year, datetime.now().month)[1]).date()
    this_month_start = datetime.combine(this_month_start, time.min)
    this_month_end = datetime.combine(this_month_end, time.max)
    this_month_data = get_data(this_month_start, this_month_end)
    data['this_month_data'] = this_month_data

    data['user'] = res_.username

    ip_count = db.session.query(LoginModel.ip, func.count(LoginModel.ip)).group_by(LoginModel.ip).all()
    top10 = sorted(ip_count, key=lambda x: x[1], reverse=True)[:10]
    data['top']=[ip for i, (ip, count) in enumerate(top10)]
    # for i, (ip, count) in enumerate(top5):
    #     print(f"第 {i+1} 名：IP 地址 {ip} 出现次数为 {count}")
    print(data)
    return render_template('index/welcome.html',data=data)


@user.route('/hotel',methods=['GET'])
def test():
    pageNum = request.args.get('pageNum', 1)
    pageSize = request.args.get('pageSize', 10)
    province = request.args.get('province')
    if province:
        query = JingDongModel.query.filter(JingDongModel.province == province).order_by(JingDongModel.sid.asc())
        total = len(JingDongModel.query.filter(JingDongModel.province== province).all())

    else:
        query = JingDongModel.query.order_by(JingDongModel.sid.asc())
        total = len(JingDongModel.query.all())
    page_objs = query.paginate(
        page=int(pageNum),
        per_page=int(pageSize),
        error_out=False,
        max_per_page=10
    ).items

    data = []
    for i in page_objs:
        data.append(i.to_dict())
    dic = {
        'data':data,
        'total':total,
        'totalPages':int((total/int(pageSize)))+1,
        'pageNum':pageNum,
        'pageSize':pageSize
    }
    print(dic)
    return render_template('index/hotel.html',data=dic)


@user.route('/api/hotel',methods=['GET'])
def hotel_api():
    """
    政策html
    """
    pageNum = request.args.get('pageNum', 1)
    pageSize = request.args.get('pageSize', 10)
    keywords = request.args.get('keywords')
    print(keywords)
    if keywords:
        query = JingDongModel.query.filter(JingDongModel.keywords==keywords).order_by(JingDongModel.sid.asc())
        total = len(JingDongModel.query.filter(JingDongModel.keywords==keywords).all())

    else:
        query = JingDongModel.query.order_by(JingDongModel.sid.asc())
        total = len(JingDongModel.query.all())
    page_objs = query.paginate(
        page=int(pageNum),
        per_page=int(pageSize),
        error_out=False,
        max_per_page=10
    ).items
    data = []
    for i in page_objs:
        data.append(i.to_dict())
    dic = {
        'data':data,
        'total':total,
        'totalPages':int((total/int(pageSize)))+1,
        'pageNum':pageNum,
        'pageSize':pageSize
    }
    print(dic)
    return jsonify({
        "data":dic
    })





