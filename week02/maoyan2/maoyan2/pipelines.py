# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymysql


# class Maoyan2Pipeline:
#     def process_item(self, item, spider):
#         return item
class MysqlPipeline():
    def __init__(self, host, database, table, user, password, port):
        self.host = host
        self.database = database
        self.table = table
        self.user = user
        self.password = password
        self.port = port

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            host=crawler.settings.get('MYSQL_HOST'),
            database=crawler.settings.get('MYSQL_DATABASE'),
            table=crawler.settings.get('MYSQL_TABLE'),
            user=crawler.settings.get('MYSQL_USER'),
            password=crawler.settings.get('MYSQL_PASSWORD'),
            port=crawler.settings.get('MYSQL_PORT'),
        )

    def open_spider(self, spider):
        self.db = pymysql.connect(self.host, self.user, self.password, self.database, charset='utf8', port=self.port)
        self.cursor = self.db.cursor()

    def close_spider(self, spider):
        self.db.close()

    def process_item(self, item, spider):
        sql_fmt = ("""INSERT INTO `{}`(`movie_id`, `name_cn`, `name_en`, `type`, `show_time`, `score`, `avatar`) 
                    VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}');""")
        sql = sql_fmt.format(self.table, item['movie_id'], item['name_cn'],
                             item['name_en'], item['type'], item['show_time'],
                             item['score'], item['avatar'],
                             )
        self.cursor.execute(sql)
        self.db.commit()
        return item