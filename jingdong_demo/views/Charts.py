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

from django.shortcuts import render
from flask import Blueprint, render_template, request, jsonify, make_response
import pandas as  pd
import numpy as np
from jingdong_demo.models.model import JingDongModel
from mychche import cache
charts = Blueprint('charts', __name__)

@charts.route('/bigScreen',methods=['GET'])
@cache.cached(timeout=31622400)  # 缓存结果一年
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
@cache.cached(timeout=31622400)  # 缓存结果一年
def map():
    '''大屏'''
    query = JingDongModel.query.with_entities(JingDongModel.sid,JingDongModel.cityName,JingDongModel.location).order_by("sid")

    pd_data = pd.read_sql(query.statement, query.session.bind)

    #去重 ###有问题
    pd_data = pd_data.dropna()

    address_num=[]

    #计算城市数量/map
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
@cache.cached(timeout=31622400)  # 缓存结果一年
def brandTop():
    '''品牌top15'''
    query = JingDongModel.query.with_entities(JingDongModel.sid,JingDongModel.cityName,JingDongModel.brandName).order_by("sid")

    pd_data = pd.read_sql(query.statement, query.session.bind)

    brand_counts = pd_data.groupby('brandName').size().drop('其他').sort_values(ascending=False).head(15)
    brand_dict = OrderedDict(brand_counts.items())

    response = json.dumps({'code': 200, 'data': brand_dict}, ensure_ascii=False, sort_keys=False)
    return response

@charts.route('/grade',methods=['GET'])
@cache.cached(timeout=31622400)  # 缓存结果一年
def grade():
    '''等级图'''
    query = JingDongModel.query.with_entities(JingDongModel.sid,JingDongModel.grade).order_by("sid")

    pd_data = pd.read_sql(query.statement, query.session.bind)

    data = pd_data.groupby('grade').size().to_dict()

    response = json.dumps({'code': 200, 'data': data}, ensure_ascii=False, sort_keys=False)
    return response

@charts.route('/radar',methods=['GET'])
@cache.cached(timeout=31622400)  # 缓存结果一年
def radar():
    '''雷达图 '''
    # 查询 amenities 列，按 sid 排序
    query = JingDongModel.query.with_entities(JingDongModel.amenities).order_by("sid")
    # 定义计数器，用于统计每个 amenity 出现的次数
    amenities_counter = Counter()
    # 遍历查询结果，每次处理1000条记录
    for amenities_str, in query.yield_per(1000):
        # 将 amenities 列按 '|' 分隔成列表，然后加入计数器
        amenities_counter.update(amenities_str.split('|'))
    # 取出出现次数最多的 5 个 amenity
    amenities_top5 = amenities_counter.most_common(5)
    # 计算最大值，向上取整到千位
    max_value = (max(dict(amenities_top5).values()) // 1000 + 1) * 1000
    # 将结果转换为 JSON 格式，并返回
    response = json.dumps({'code': 200, 'data': amenities_top5, "maxNum": max_value}, ensure_ascii=False, sort_keys=False)
    return response


@charts.route('/brandAvgPrice',methods=['GET'])
@cache.cached(timeout=31622400)  # 缓存结果一年
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

# 商圈Top5
@charts.route('/businessZone',methods=['GET'])
def calculate_correlation():
    # 使用query方法查询数据
    query = JingDongModel.query.with_entities(JingDongModel.sid,JingDongModel.businessZoneName).order_by("sid")
    # 将数据转换为DataFrame格式
    data = pd.read_sql(query.statement, query.session.bind)
    # 获取出现次数最多的前三个品牌名称
    top_brands = data['businessZoneName'].value_counts().drop('').nlargest(8).to_dict()
    # print(top_brands)
    response = json.dumps({'code': 200, 'data': top_brands, }, ensure_ascii=False, sort_keys=False)
    return response