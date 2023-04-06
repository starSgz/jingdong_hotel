# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
import os
import logging
import pymysql
import scrapy
from scrapy.pipelines.images import ImagesPipeline
class HotelCrawlPipeline:
    def __init__(self, host, db, port, user, password):
        self.host = host
        self.db = db
        self.port = port
        self.user = user
        self.password = password
        self.connect = pymysql.connect(host=self.host, user=self.user, password=self.password, db=self.db, port=self.port, charset='utf8')
        self.cursor = self.connect.cursor()
        logging.info('数据库连接成功 => %s' + '主机：', self.host + ' 端口：' + self.db)

    @classmethod
    def from_crawler(cls, crawler):
        db_name = crawler.settings.get('DB_SETTINGS')
        db_params = db_name.get('db1')
        return cls(
            host=db_params.get('host'),
            db=db_params.get('db'),
            user=db_params.get('user'),
            password=db_params.get('password'),
            port=db_params.get('port'),
        )

    def process_item(self, item, spider):

        table_fields = item.get('table_fields')
        table_name = item.get('table_name')
        if table_fields is None or table_name is None:
            raise Exception('必须要传表名table_name和字段名table_fields，表名或者字段名不能为空')
        values_params = '%s, ' * (len(table_fields) - 1) + '%s'
        keys = ', '.join(table_fields)
        values = ['%s' % str(item.get(i, '')) for i in table_fields]
        insert_sql = 'insert into %s (%s) values (%s)' % (table_name, keys, values_params)
        try:
            self.cursor.execute(insert_sql, tuple(values))
            logging.info("数据插入成功 => " + '1' + f'##名字：{item["name"]}###价格：{item["price"]}###城市：{item["cityName"]}')
        except Exception as e:
            logging.error("执行sql异常 => " + str(e))
            try:
                # 检查连接是否断开，如果断开就进行重连
                self.connect.ping(reconnect=True)
            except Exception as e:
                print("操作出现错误：{}".format(e))
                self.connect.rollback()
        finally:
            # 要提交，不提交无法保存到数据库
            self.connect.commit()
            try:
                # 检查连接是否断开，如果断开就进行重连
                self.connect.ping(reconnect=True)
            except Exception as e:
                print("操作出现错误：{}".format(e))
                self.connect.rollback()
        return item

    def close_spider(self, spider):
        self.connect.close()
        self.cursor.close()

class MyImagesPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        yield scrapy.Request(url = item['coverImageUrl'],meta={'item':item})

    def file_path(self, request, response=None, info=None):
        item = request.meta['item']
        save_path = "imges/{}/{}".format(item["province"],item["cityName"])
        # 文件没有存在就创建
        if not os.path.exists(save_path):
            os.makedirs(save_path)
        path = '{}/{}'.format(save_path, request.url.split('/')[-1])
        return path

    def item_completed(self, results, item, info):
        # 将图片的本地路径保存在item中
        item['image_paths'] = "".join([x['path'] for ok, x in results if ok])
        return item
