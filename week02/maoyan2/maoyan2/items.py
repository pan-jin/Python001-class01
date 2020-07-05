# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy 
from scrapy import Field, Item


class Maoyan2Item(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    movie_id = Field()
    name_cn = Field()
    name_en = Field()
    type = Field()
    show_time = Field()
    score = Field()
    avatar = Field()
