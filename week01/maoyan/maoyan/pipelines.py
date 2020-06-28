# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pandas as pd


class MaoyanPipeline:
    def process_item(self, item, spider):
        title = item['title']
        type = item['type']
        time = item['time']
        movie_info = [[title, type, time]]
        df = pd.DataFrame(movie_info, columns=['title', 'type', 'time'])
        df.to_csv('./movies.csv',mode='a',encoding='utf8',index=False,header=False)
        return item