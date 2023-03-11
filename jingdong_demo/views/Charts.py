# -*- coding: utf-8 -*-
"""
@Time ： 2023/3/10 21:30
@Auth ： star
@File ：Charts.py
"""
import ast
import json
import math
from collections import OrderedDict, Counter

from flask import Blueprint, render_template, request, jsonify, make_response
import pandas as  pd
import numpy as np
from jingdong_demo.models.model import JingDongModel

charts = Blueprint('charts', __name__)


@charts.route('/bigScreen',methods=['GET'])
def bigScreen():
    '''大屏'''
    query = JingDongModel.query.with_entities(JingDongModel.sid,JingDongModel.cityName,JingDongModel.score,
                                              JingDongModel.cityName,JingDongModel.brandName).order_by("sid")
    pd_data = pd.read_sql(query.statement, query.session.bind)

    #总数量
    allcount = len(pd_data)
    #品牌数
    pd_data_brand=pd_data['brandName']
    pd_data_brand.drop_duplicates(keep='last',inplace=True)
    brandNum = pd_data_brand.count()

    #平均得分
    pd_data_score = pd_data
    pd_data_score['score'] = pd.to_numeric(pd_data_score['score'],errors='coerce')
    pd_data_score.dropna(subset=['score'],inplace=True)
    avgScore = pd_data_score['score'].mean()

    #酒店最多的城市
    hotelMax = pd_data.groupby('cityName').size().nlargest(1).to_dict()



    data = {"allcount":allcount,'brandNum':brandNum,'avgScore':round(avgScore,2),'hotelMax':hotelMax}
    print(data)



    return render_template('chart/bigScreen.html',data=data)


@charts.route('/map',methods=['GET'])
def map():
    '''大屏'''
    query = JingDongModel.query.with_entities(JingDongModel.sid,JingDongModel.cityName,JingDongModel.location).order_by("sid")

    pd_data = pd.read_sql(query.statement, query.session.bind)

    #去重 ###有问题
    pd_data = pd_data.dropna()

    address_num=[]

    #计算城市数量
    city_list = list(pd_data.groupby('cityName').count().index)
    count_list = list(pd_data.groupby('cityName').count().location)
    for k,v in zip(city_list,count_list):
        address_num.append({"name":k, "value":v})

    #获取城市经纬度
    dic = {}

    for i in city_list:
        #转字典
        res = ast.literal_eval(pd_data.loc[pd_data['cityName'] == i].iloc[0]['location'])
        dic[i]=[res.get("lon"),res.get("lat")]

    result = {"data":address_num,"geoCoordMap":dic}

    return jsonify({
        "code":200,
        "data":result
    })

@charts.route('/brandTop',methods=['GET'])
def brandTop():
    '''品牌top15'''
    query = JingDongModel.query.with_entities(JingDongModel.sid,JingDongModel.cityName,JingDongModel.brandName).order_by("sid")

    pd_data = pd.read_sql(query.statement, query.session.bind)

    brand_counts = pd_data.groupby('brandName').size().drop('其他').sort_values(ascending=False).head(15)
    brand_dict = OrderedDict(brand_counts.items())

    response = json.dumps({'code': 200, 'data': brand_dict}, ensure_ascii=False, sort_keys=False)
    return response

@charts.route('/grade',methods=['GET'])
def grade():
    '''等级图'''
    query = JingDongModel.query.with_entities(JingDongModel.sid,JingDongModel.grade).order_by("sid")

    pd_data = pd.read_sql(query.statement, query.session.bind)

    data = pd_data.groupby('grade').size().to_dict()

    response = json.dumps({'code': 200, 'data': data}, ensure_ascii=False, sort_keys=False)
    return response

@charts.route('/radar',methods=['GET'])
def radar():
    '''雷达图'''
    query = JingDongModel.query.with_entities(JingDongModel.sid,JingDongModel.amenities).order_by("sid")

    pd_data = pd.read_sql(query.statement, query.session.bind)
    print(Counter(pd_data['amenities'].str.split('|').sum()))
    amenities_counter = Counter(pd_data['amenities'].str.split('|').sum()).most_common(5)
    max_value = int(math.ceil(max(dict(amenities_counter).values()) / 1000)) * 1000
    response = json.dumps({'code': 200, 'data': amenities_counter,"maxNum":max_value}, ensure_ascii=False, sort_keys=False)
    return response


@charts.route('/brandAvgPrice',methods=['GET'])
def brandAvgPrice():
    '''品牌价格'''
    query = JingDongModel.query.with_entities(JingDongModel.sid,JingDongModel.brandName,JingDongModel.price).order_by("sid")
    pd_data = pd.read_sql(query.statement, query.session.bind)
    pd_data['price'] = pd.to_numeric(pd_data['price'], errors='coerce')
    # 获取出现次数最多的前三个品牌名称
    top_brands = pd_data['brandName'].value_counts().head(10).index.tolist()
    # 计算这些品牌的平均价格
    avg_prices = pd_data[pd_data['brandName'].isin(top_brands)].groupby('brandName')['price'].mean().round(2)
    # 将 Series 转换成字典
    avg_prices_dict = avg_prices.to_dict()
    response = json.dumps({'code': 200, 'data': avg_prices_dict,}, ensure_ascii=False, sort_keys=False)

    return response