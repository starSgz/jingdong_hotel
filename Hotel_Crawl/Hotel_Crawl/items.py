# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class HotelCrawlItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    address = scrapy.Field() #详细地点
    name = scrapy.Field() #酒店名字
    cityName = scrapy.Field() #城市名字
    districtName = scrapy.Field() #地区名字
    brandName = scrapy.Field() #酒店品牌名字 没有品牌就为其他
    totalComments = scrapy.Field() #酒店评论数量
    score = scrapy.Field() #酒店评分
    location = scrapy.Field() #酒店位置 坐标
    price = scrapy.Field() #酒店最低价格
    coverImageUrl = scrapy.Field() #酒店封面链接
    amenities = scrapy.Field() #酒店便利设施
    detailPage_url = scrapy.Field() #酒店详细页
    grade = scrapy.Field() #酒店等级
    checkInDate = scrapy.Field() #入住时间
    checkOutDate = scrapy.Field() #离开时间
    businessZoneName = scrapy.Field() #酒店附近商圈
    province = scrapy.Field() #省份
    image_paths = scrapy.Field() #图片地址
    table_fields = scrapy.Field() #表的字段
    table_name = scrapy.Field() #表的名字
