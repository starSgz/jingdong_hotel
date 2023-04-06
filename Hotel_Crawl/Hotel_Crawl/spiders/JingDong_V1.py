# import json
# import scrapy
# from Hotel_Crawl.items import HotelCrawlItem
# from Hotel_Crawl.settings import PROVINCES
# import datetime
# class JingdongV1Spider(scrapy.Spider):
#     name = 'JingDong_V1'
#     # allowed_domains = ['hotel.jd.com']
#     # start_urls = ['http://hotel.jd.com/']
#
#     def start_requests(self):
#         with open("cityList.json","r",encoding="utf-8")as f:
#             datas = json.load(f)["body"]
#         for index,citys_list in datas.items():
#             if(index=="HOT"):
#                 continue
#             for city in citys_list:
#                 city_name = city[1]
#                 city_id = str(city[0])
#                 # print(city_id,city_name)
#                 today = datetime.date.today() + datetime.timedelta(days=1)
#                 secondDay = datetime.date.today() + datetime.timedelta(days=1)
#                 url ="https://hotel.jd.com/api/json/getHotelList"
#                 data ={
#                     "keyword": "",
#                     "cityId": city_id,
#                     "checkInDate": today,
#                     "checkOutDate": secondDay,
#                     "minPrice": "",
#                     "maxPrice": "",
#                     "stars": "",
#                     "pageSize": "30",
#                     "pageNum": "1",
#                     "bedType": "",
#                     "amenities": "",
#                     "promotions": "",
#                     "themes": "",
#                     "breakfast": "",
#                     "order": "",
#                     "agreementHotel": "0",
#                     "payMode": "",
#                     "poi": "%5B%5D",
#                     "channel": "1010"
#                 }
#                 yield scrapy.FormRequest(url=url,formdata=data,callback=self.parse,meta={"data":data,"city_name":city_name})
#                 # break;
#
#     def parse(self, response):
#         data = response.meta["data"]
#         city_name = response.meta["city_name"]
#         body_list = response.json()["body"]["list"]
#         for hotel_data in body_list:
#             items = HotelCrawlItem()
#             items["checkInDate"] = data["checkInDate"]
#             items["checkOutDate"] = data["checkOutDate"]
#             items["address"] = hotel_data["address"]
#             items["name"] = hotel_data["name"]
#             items["cityName"] = city_name
#             items["districtName"] = hotel_data["districtName"] if hotel_data["districtName"] is not None else hotel_data["cityName"]
#             items["brandName"] = hotel_data["brandName"] if hotel_data["brandName"] is not None else "其他"
#             items["totalComments"] = hotel_data["totalComments"]
#             items["score"] = hotel_data["score"]
#             items["location"] = hotel_data["location"]
#             items["price"] = hotel_data["price"]
#             items["coverImageUrl"] = hotel_data["coverImageUrl"]
#             # 遍历设施映射字典
#             amenities_map = [
#                 {
#                     "code": 1,
#                     "name": "免费wifi"
#                 },
#                 {
#                     "code": 2,
#                     "name": "停车场"
#                 },
#                 {
#                     "code": 3,
#                     "name": "健身室"
#                 },
#                 {
#                     "code": 4,
#                     "name": "游泳池"
#                 },
#                 {
#                     "code": 5,
#                     "name": "餐厅"
#                 },
#                 {
#                     "code": 6,
#                     "name": "温泉"
#                 },
#                 {
#                     "code": 7,
#                     "name": "SPA"
#                 },
#                 {
#                     "code": 8,
#                     "name": "酒吧"
#                 },
#                 {
#                     "code": 10,
#                     "name": "行李寄存"
#                 },
#                 {
#                     "code": 11,
#                     "name": "接机服务"
#                 },
#                 {
#                     "code": 12,
#                     "name": "会议厅"
#                 }
#             ]
#             try:
#                 items["amenities"] = []
#                 for aM in amenities_map:
#                     if(aM["code"] in hotel_data["amenities"]):
#                         items["amenities"].append(aM["name"])
#                 items["amenities"] = '|'.join(items["amenities"])
#             except TypeError:
#                 items["amenities"] = ''
#             # 详细页url
#             items["detailPage_url"] = f'https://hotel.jd.com/detail?hotelId={hotel_data["hotelId"]}'
#             # 酒店等级
#             grade_map = {"2":"经济/简约","3":"经济/简约","4":"四星/高档","5":"五星/豪华"}
#             items["grade"] = grade_map[str(hotel_data["grade"])]
#             # 酒店附近商圈
#             try:
#                 items["businessZoneName"] = []
#                 for businessZone in hotel_data["businessZoneList"]:
#                     items["businessZoneName"].append(businessZone["businessZoneName"])
#                 items["businessZoneName"] = '|'.join(items["businessZoneName"])
#             except TypeError:
#                 items["businessZoneName"] = ''
#             items["province"] = self.get_province(items["cityName"])
#             # print(items)
#             items['table_fields'] = ['address','name','cityName','districtName','brandName','totalComments','score','location','price','coverImageUrl','amenities','detailPage_url','grade','checkInDate','checkOutDate','businessZoneName','province','image_paths']
#             items['table_name'] = "JingDong"
#             yield items
#
#     def get_province(self,city_name):
#         '''输入城市返回对应的省份'''
#         for PROVINCE, citys in PROVINCES.items():
#             if (PROVINCE == "all"):
#                 continue
#             if city_name + "市" in citys:
#                 return PROVINCE
#             elif city_name in citys:
#                 return PROVINCE
#
# if __name__ == '__main__':
#     from scrapy import cmdline
#     cmdline.execute("scrapy crawl JingDong_V1".split())