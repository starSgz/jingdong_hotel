# -*- coding: utf-8 -*-
"""
@Time ： 2023/3/9 22:56
@Auth ： star
@File ：test.py
"""
import requests
from lxml import etree

# 搜索关键字
keyword = '手机'

# 构建请求URL
url = 'https://s.taobao.com/search?q=' + keyword

# 发送请求并获取响应HTML内容
response = requests.get(url)
html_content = response.text

# 解析HTML内容
selector = etree.HTML(html_content)

# 提取商品名和价格
items = selector.xpath('//div[@class="item J_MouserOnverReq"]')
for item in items:
    name = item.xpath('.//div[@class="title"]/text()')[0]
    price = item.xpath('.//strong[@class="price"]/text()')[0]
    print(name + ' - ' + price)