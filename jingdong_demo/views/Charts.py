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
import pandas as pd
import numpy as np
from jingdong_demo.models.model import JingDongModel
from mychche import cache

charts = Blueprint('charts', __name__)
provinces = ['河北', '山西', '内蒙古', '辽宁', '吉林', '黑龙江', '江苏', '浙江', '安徽', '福建', '江西', '山东', '河南', '湖北', '湖南', '广东', '广西', '海南', '四川', '贵州', '云南', '西藏', '陕西', '甘肃', '青海', '宁夏', '新疆', '台湾']
'''大屏'''
@charts.route('/bigScreen', methods=['GET'])
@cache.cached(timeout=31622400, make_cache_key=lambda *args, **kwargs: request.url)  # 缓存结果一年
def bigScreen():
    query = JingDongModel.query.with_entities(JingDongModel.sid, JingDongModel.cityName, JingDongModel.score,JingDongModel.brandName).order_by("sid")
    pd_data = pd.read_sql(query.statement, query.session.bind)
    # 总数量
    allcount = len(pd_data)
    # 品牌数
    pd_data_brand = pd_data['brandName']
    pd_data_brand.drop_duplicates(keep='last', inplace=True)
    brandNum = pd_data_brand.count()
    # 平均得分
    pd_data_score = pd_data
    pd_data_score['score'] = pd.to_numeric(pd_data_score['score'], errors='coerce')
    pd_data_score.dropna(subset=['score'], inplace=True)
    avgScore = pd_data_score['score'].mean()
    # 酒店最多的城市
    hotelMax = pd_data.groupby('cityName').size().nlargest(1).to_dict()

    data = {"allcount": allcount, 'brandNum': brandNum, 'avgScore': round(avgScore, 2), 'hotelMax': hotelMax}
    print(data)
    return render_template('chart/bigScreen.html', data=data)


'''中国地图'''
@charts.route('/map', methods=['GET'])
@cache.cached(timeout=31622400, make_cache_key=lambda *args, **kwargs: request.url)  # 缓存结果一年
def map():
    query = JingDongModel.query.with_entities(JingDongModel.sid, JingDongModel.cityName, JingDongModel.brandName,JingDongModel.businessZoneName, JingDongModel.grade,JingDongModel.location).order_by("sid")
    pd_data = pd.read_sql(query.statement, query.session.bind)
    businessZoneName = request.args.get('businessZoneName')  # 商圈
    brandName = request.args.get('brandName')  # 品牌
    grade = request.args.get('grade')  # 星级
    # 条件筛选
    if businessZoneName is not None:
        pd_data = pd_data[pd_data['businessZoneName'] == businessZoneName]
        print(pd_data)
    if brandName is not None:
        pd_data = pd_data[pd_data['brandName'] == brandName]
        print(pd_data)
    if grade is not None:
        pd_data = pd_data[pd_data['grade'] == grade]
        print(pd_data)

    # 去重 ###有问题
    pd_data = pd_data.dropna()
    address_num = []
    # 计算城市数量/map
    city_list = list(pd_data.groupby('cityName').count().index)
    count_list = list(pd_data.groupby('cityName').count().location)
    for k, v in zip(city_list, count_list):
        address_num.append({"name": k, "value": v})

    # 获取城市经纬度
    dic = {}
    for i in city_list:
        # 转字典
        res = ast.literal_eval(pd_data.loc[pd_data['cityName'] == i].iloc[0]['location'])
        dic[i] = [res.get("lon"), res.get("lat")]

    result = {"data": address_num, "geoCoordMap": dic}
    return jsonify({
        "code": 200,
        "data": result
    })


'''品牌top15'''
@charts.route('/brandTop', methods=['GET'])
@cache.cached(timeout=31622400, make_cache_key=lambda *args, **kwargs: request.url)  # 缓存结果一年
def brandTop():
    cityName = request.args.get('cityName')  # 城市
    businessZoneName = request.args.get('businessZoneName')  # 商圈
    grade = request.args.get('grade')  # 星级
    query = JingDongModel.query.with_entities(JingDongModel.sid, JingDongModel.cityName, JingDongModel.brandName,JingDongModel.province,
                                              JingDongModel.businessZoneName, JingDongModel.grade).order_by("sid")
    pd_data = pd.read_sql(query.statement, query.session.bind)
    # 条件筛选
    if cityName is not None:
        if cityName in provinces:
            pd_data = pd_data[pd_data['province'].str.contains(cityName)]
        else:
            pd_data = pd_data[pd_data['cityName'] == cityName]
    if businessZoneName is not None:
        pd_data = pd_data[pd_data['businessZoneName'] == businessZoneName]
        print(pd_data)
    if grade is not None:
        pd_data = pd_data[pd_data['grade'] == grade]
        print(pd_data)

    brand_counts = pd_data.groupby('brandName').size().drop('其他').sort_values(ascending=False).head(15)
    brand_dict = OrderedDict(brand_counts.items())
    response = json.dumps({'code': 200, 'data': brand_dict}, ensure_ascii=False, sort_keys=False)
    return response


'''等级图 星级占比'''
@charts.route('/grade', methods=['GET'])
@cache.cached(timeout=31622400, make_cache_key=lambda *args, **kwargs: request.url)  # 缓存结果一年
def grade():
    cityName = request.args.get('cityName')  # 城市
    businessZoneName = request.args.get('businessZoneName')  # 商圈
    brandName = request.args.get('brandName')  # 品牌
    query = JingDongModel.query.with_entities(JingDongModel.sid,JingDongModel.province,  JingDongModel.cityName, JingDongModel.brandName,JingDongModel.businessZoneName, JingDongModel.grade).order_by("sid")
    pd_data = pd.read_sql(query.statement, query.session.bind)
    # 条件筛选
    if cityName is not None:
        if cityName in provinces:
            pd_data = pd_data[pd_data['province'].str.contains(cityName)]
        else:
            pd_data = pd_data[pd_data['cityName'] == cityName]
    if businessZoneName is not None:
        pd_data = pd_data[pd_data['businessZoneName'] == businessZoneName]
        print(pd_data)
    if brandName is not None:
        pd_data = pd_data[pd_data['brandName'] == brandName]
        print(pd_data)
    data = pd_data.groupby('grade').size().to_dict()
    response = json.dumps({'code': 200, 'data': data}, ensure_ascii=False, sort_keys=False)
    return response


'''雷达图 设施配备'''
@charts.route('/radar', methods=['GET'])
@cache.cached(timeout=31622400, make_cache_key=lambda *args, **kwargs: request.url)  # 缓存结果一年
def radar():
    # 查询 amenities 列，按 sid 排序
    cityName = request.args.get('cityName')  # 城市
    businessZoneName = request.args.get('businessZoneName')  # 商圈
    brandName = request.args.get('brandName')  # 品牌
    grade = request.args.get('grade')  # 星级
    # 条件筛选
    vars = [cityName,businessZoneName,brandName,grade]
    if all(var is None for var in vars):
        query = JingDongModel.query.with_entities(JingDongModel.amenities).order_by("sid")
    if cityName is not None:
        if cityName is not None:
            if cityName in provinces:
                query = JingDongModel.query.filter(JingDongModel.province.like('%' + cityName + '%')).with_entities(JingDongModel.amenities).order_by("sid")
            else:
                query = JingDongModel.query.filter(JingDongModel.cityName == cityName).with_entities(JingDongModel.amenities).order_by("sid")
    if businessZoneName is not None:
        query = JingDongModel.query.filter(JingDongModel.businessZoneName == businessZoneName).with_entities(JingDongModel.amenities).order_by("sid")
    if brandName is not None:
        query = JingDongModel.query.filter(JingDongModel.brandName == brandName).with_entities(JingDongModel.amenities).order_by("sid")
    if grade is not None:
        query = JingDongModel.query.filter(JingDongModel.grade == grade).with_entities(JingDongModel.amenities).order_by("sid")

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
    response = json.dumps({'code': 200, 'data': amenities_top5, "maxNum": max_value}, ensure_ascii=False,
                          sort_keys=False)
    return response


'''数量Top10的品牌酒店的均价'''
@charts.route('/brandAvgPrice', methods=['GET'])
@cache.cached(timeout=31622400, make_cache_key=lambda *args, **kwargs: request.url)  # 缓存结果一年
def brandAvgPrice():
    query = JingDongModel.query.with_entities(JingDongModel.sid, JingDongModel.province, JingDongModel.cityName, JingDongModel.brandName,JingDongModel.businessZoneName, JingDongModel.grade, JingDongModel.price).order_by("sid")
    pd_data = pd.read_sql(query.statement, query.session.bind)
    cityName = request.args.get('cityName')  # 城市
    businessZoneName = request.args.get('businessZoneName')  # 商圈
    brandName = request.args.get('brandName')  # 品牌
    grade = request.args.get('grade')  # 星级
    # 条件筛选
    if cityName is not None:
        if cityName in provinces:
            pd_data = pd_data[pd_data['province'].str.contains(cityName)]
        else:
            pd_data = pd_data[pd_data['cityName'] == cityName]
    if businessZoneName is not None:
        pd_data = pd_data[pd_data['businessZoneName'] == businessZoneName]
        print(pd_data)
    if brandName is not None:
        pd_data = pd_data[pd_data['brandName'] == brandName]
        print(pd_data)
    if grade is not None:
        pd_data = pd_data[pd_data['grade'] == grade]
        print(pd_data)

    pd_data['price'] = pd.to_numeric(pd_data['price'], errors='coerce')
    # 获取出现次数最多的前10个品牌名称
    top_brands = pd_data['brandName'].value_counts().head(10).index.tolist()
    # 计算这些品牌的平均价格
    avg_prices = pd_data[pd_data['brandName'].isin(top_brands)].groupby('brandName')['price'].mean().round(2)
    # 将 Series 转换成字典
    avg_prices_dict = avg_prices.to_dict()
    response = json.dumps({'code': 200, 'data': avg_prices_dict, }, ensure_ascii=False, sort_keys=False)
    return response


'''商圈Top8'''
@charts.route('/businessZone', methods=['GET'])
@cache.cached(timeout=31622400, make_cache_key=lambda *args, **kwargs: request.url)  # 缓存结果一年
def calculate_correlation():
    # 使用query方法查询数据
    query = JingDongModel.query.with_entities(JingDongModel.sid, JingDongModel.province, JingDongModel.cityName, JingDongModel.brandName,JingDongModel.businessZoneName, JingDongModel.grade).order_by("sid")
    # 将数据转换为DataFrame格式
    pd_data = pd.read_sql(query.statement, query.session.bind)
    cityName = request.args.get('cityName')  # 城市
    brandName = request.args.get('brandName')  # 品牌
    grade = request.args.get('grade')  # 星级
    # 条件筛选
    if cityName is not None:
        if cityName in provinces:
            pd_data = pd_data[pd_data['province'].str.contains(cityName)]
        else:
            pd_data = pd_data[pd_data['cityName'] == cityName]
    if brandName is not None:
        pd_data = pd_data[pd_data['brandName'] == brandName]
        print(pd_data)
    if grade is not None:
        pd_data = pd_data[pd_data['grade'] == grade]
        print(pd_data)
    # 获取出现次数最多的前三个品牌名称
    top_brands = pd_data['businessZoneName'].value_counts().drop('').nlargest(8).to_dict()
    # print(top_brands)
    response = json.dumps({'code': 200, 'data': top_brands, }, ensure_ascii=False, sort_keys=False)
    return response


'''大屏左上角 统计功能'''
@charts.route('/dataStatistics', methods=['GET'])
@cache.cached(timeout=31622400, make_cache_key=lambda *args, **kwargs: request.url)  # 缓存结果一年
def dataStatistics():
    query = JingDongModel.query.with_entities(JingDongModel.sid, JingDongModel.province, JingDongModel.cityName, JingDongModel.brandName,JingDongModel.businessZoneName, JingDongModel.grade,JingDongModel.score).order_by("sid")
    pd_data = pd.read_sql(query.statement, query.session.bind)
    cityName = request.args.get('cityName')  # 城市
    businessZoneName = request.args.get('businessZoneName')  # 商圈
    brandName = request.args.get('brandName')  # 品牌
    grade = request.args.get('grade')  # 星级
    screeningCondition = ''
    # 条件筛选
    if cityName is not None:
        if cityName in provinces:
            pd_data = pd_data[pd_data['province'].str.contains(cityName)]
        else:
            pd_data = pd_data[pd_data['cityName'] == cityName]
        screeningCondition = cityName
    if businessZoneName is not None:
        pd_data = pd_data[pd_data['businessZoneName'] == businessZoneName]
        screeningCondition = businessZoneName
        print(pd_data)
    if brandName is not None:
        pd_data = pd_data[pd_data['brandName'] == brandName]
        screeningCondition = brandName
        print(pd_data)
    if grade is not None:
        pd_data = pd_data[pd_data['grade'] == grade]
        screeningCondition = grade
        print(pd_data)

    # 总数量
    allcount = len(pd_data)
    # 品牌数
    pd_data_brand = pd_data['brandName']
    pd_data_brand.drop_duplicates(keep='last', inplace=True)
    brandNum = pd_data_brand.count()
    # 平均得分
    pd_data_score = pd_data
    pd_data_score['score'] = pd.to_numeric(pd_data_score['score'], errors='coerce')
    pd_data_score.dropna(subset=['score'], inplace=True)
    avgScore = pd_data_score['score'].mean()
    # 酒店最多的城市
    hotelMax = pd_data.groupby('cityName').size().nlargest(1).to_dict()

    data = {"allcount": allcount, 'brandNum': int(brandNum), 'avgScore': round(avgScore, 2), 'hotelMax': hotelMax}
    print(data)
    return jsonify({
        "code": 200,
        "data": data,
        "screeningCondition":screeningCondition
    })