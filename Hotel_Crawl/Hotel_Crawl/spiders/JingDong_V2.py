import json
import scrapy
from Hotel_Crawl.items import HotelCrawlItem
from Hotel_Crawl.settings import PROVINCES
import datetime
import pymysql
from Hotel_Crawl.settings import DB_SETTINGS
class JingdongV1Spider(scrapy.Spider):
    name = 'JingDong_V2'
    # allowed_domains = ['hotel.jd.com']
    # start_urls = ['http://hotel.jd.com/']
    def start_requests(self):
        for PROVINCE, citys in PROVINCES.items():
            if (PROVINCE == "all"):
                continue
            for city_name in citys:
                url = f"https://hotel.jd.com/api/json/getDestSuggestList?searchType=0&keyword={city_name}"
                print(url)
                yield scrapy.Request(url=url,callback=self.constructRequest,meta={"PROVINCE":PROVINCE,"city_name":city_name})
            #     break;#控制城市
            # break;#控制省份

    def constructRequest(self,response):
        city_name =response.meta["city_name"]
        PROVINCE =response.meta["PROVINCE"]
        datas = response.json()["body"]
        for data in datas:
            # print(city_name,data)
            if(city_name.__contains__(data["cityName"])):
                city_id = data["cityCode"]
                today = datetime.date.today()
                secondDay = datetime.date.today() + datetime.timedelta(days=1)
                url = "https://hotel.jd.com/api/json/getHotelList"
                data = {
                    "keyword": "",
                    "cityId": str(city_id),
                    "checkInDate": str(today),
                    "checkOutDate": str(secondDay),
                    "minPrice": "0",
                    "maxPrice": "100000",
                    "stars": "",
                    "pageSize": "30",
                    "pageNum": "1",
                    "bedType": "",
                    "amenities": "",
                    "promotions": "",
                    "themes": "",
                    "breakfast": "",
                    "order": "",
                    "agreementHotel": "0",
                    "payMode": "",
                    "poi": "%5B%5D",
                    "channel": "1010"
                }
                yield scrapy.FormRequest(url=url, formdata=data, callback=self.parse,meta={"data": data, "city_name": city_name,"PROVINCE":PROVINCE})
                break



    def parse(self, response):
        '''处理获取到的数据'''
        data = response.meta["data"]
        city_name = response.meta["city_name"]
        PROVINCE = response.meta["PROVINCE"]
        # print(f'*******当前正在爬取第{str(response.json()["body"]["pageNum"])}页面******')
        print(response.json())
        body_list = response.json()["body"]["list"]
        for hotel_data in body_list:
            items = HotelCrawlItem()
            items["checkInDate"] = data["checkInDate"]
            items["checkOutDate"] = data["checkOutDate"]
            items["address"] = hotel_data["address"]
            items["name"] = hotel_data["name"]
            items["cityName"] = city_name
            items["districtName"] = hotel_data["districtName"] if hotel_data["districtName"] is not None else hotel_data["cityName"]
            items["brandName"] = hotel_data["brandName"] if hotel_data["brandName"] is not None else "其他"
            items["totalComments"] = hotel_data["totalComments"]
            items["score"] = hotel_data["score"]
            items["location"] = hotel_data["location"]
            items["price"] = hotel_data["price"]
            default_image = "https://img10.360buyimg.com/hotel/s645x376_jfs/t18118/23/458849392/87404/cb108d8b/5a7acf23Nb19c4919.jpg"
            items["coverImageUrl"] = hotel_data["coverImageUrl"] if hotel_data["coverImageUrl"] is not None else default_image
            # 遍历设施映射字典
            amenities_map = [
                {
                    "code": 1,
                    "name": "免费wifi"
                },
                {
                    "code": 2,
                    "name": "停车场"
                },
                {
                    "code": 3,
                    "name": "健身室"
                },
                {
                    "code": 4,
                    "name": "游泳池"
                },
                {
                    "code": 5,
                    "name": "餐厅"
                },
                {
                    "code": 6,
                    "name": "温泉"
                },
                {
                    "code": 7,
                    "name": "SPA"
                },
                {
                    "code": 8,
                    "name": "酒吧"
                },
                {
                    "code": 10,
                    "name": "行李寄存"
                },
                {
                    "code": 11,
                    "name": "接机服务"
                },
                {
                    "code": 12,
                    "name": "会议厅"
                }
            ]
            try:
                items["amenities"] = []
                for aM in amenities_map:
                    if(aM["code"] in hotel_data["amenities"]):
                        items["amenities"].append(aM["name"])
                items["amenities"] = '|'.join(items["amenities"])
            except TypeError:
                items["amenities"] = ''
            # 详细页url
            items["detailPage_url"] = f'https://hotel.jd.com/detail?hotelId={hotel_data["hotelId"]}'
            # 酒店等级
            grade_map = {"2":"经济/简约","3":"经济/简约","4":"四星/高档","5":"五星/豪华","-1":"其他"}
            items["grade"] = grade_map[str(hotel_data["grade"])]
            # 酒店附近商圈
            try:
                items["businessZoneName"] = []
                for businessZone in hotel_data["businessZoneList"]:
                    items["businessZoneName"].append(businessZone["businessZoneName"])
                items["businessZoneName"] = '|'.join(items["businessZoneName"])
            except TypeError:
                items["businessZoneName"] = ''
            items["province"] = PROVINCE
            # print(items)
            items['table_fields'] = ['address','name','cityName','districtName','brandName','totalComments','score','location','price','coverImageUrl','amenities','detailPage_url','grade','checkInDate','checkOutDate','businessZoneName','province','image_paths']
            items['table_name'] = "JingDong2"
            # 去重
            DuplicatesNum = self.RemoveDuplicates(items['detailPage_url'])
            if DuplicatesNum != 0:
                self.logger.info('{}报告已入库'.format(items["detailPage_url"]))
                continue
            yield items

        # 下一页
        if(response.json()["body"]["pageNum"]==1):
            page = response.json()["body"]["pages"]
            print(f"{city_name}一共 ：{page}页！！！")
            for pageNum in range(2,page+1):
                city_id = data["cityId"]
                today = datetime.date.today()
                secondDay = datetime.date.today() + datetime.timedelta(days=1)
                url = "https://hotel.jd.com/api/json/getHotelList"
                data = {
                    "keyword": "",
                    "cityId": str(city_id),
                    "checkInDate": str(today),
                    "checkOutDate": str(secondDay),
                    "minPrice": "0",
                    "maxPrice": "100000",
                    "stars": "",
                    "pageSize": "30",
                    "pageNum": str(pageNum),
                    "bedType": "",
                    "amenities": "",
                    "promotions": "",
                    "themes": "",
                    "breakfast": "",
                    "order": "",
                    "agreementHotel": "0",
                    "payMode": "",
                    "poi": "%5B%5D",
                    "channel": "1010"
                }
                yield scrapy.FormRequest(url=url, formdata=data, callback=self.parse,meta={"data": data, "city_name": city_name,"PROVINCE":PROVINCE})

    def RemoveDuplicates(self,detailPage_url):
        # 去重
        db = pymysql.Connect(
            host=DB_SETTINGS["db1"]["host"],
            user=DB_SETTINGS["db1"]["user"],
            passwd=DB_SETTINGS["db1"]["password"],
            db=DB_SETTINGS["db1"]["db"],
            port=DB_SETTINGS["db1"]["port"],
            charset='utf8',
            cursorclass=pymysql.cursors.DictCursor  # 返回结果转成字典（dictionary）
        )
        # 如果想要操作数据库，还需要获取db上的cursor对象
        cursor = db.cursor()
        # 使用cursor.execute来执行sql语句
        cursor.execute(f'SELECT name FROM jingdong2 WHERE detailPage_url="{detailPage_url}"')
        rs = cursor.fetchall()
        DuplicatesNum = len(rs)
        cursor.close()
        db.close()
        return DuplicatesNum
if __name__ == '__main__':
    from scrapy import cmdline
    cmdline.execute("scrapy crawl JingDong_V2".split())