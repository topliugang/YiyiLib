# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from YiyiSqlite3 import Sqlite3db

# 原则：数据全部为字符串，list，dict等转换成json字符串

class YiyiItem(scrapy.Item):
    def select(self, sql):


# select insert update delete
class XinyuBook(scrapy.Item):
    bookid = scrapy.Field()
    detail_url = scrapy.Field()
    full_detail_url = scrapy.Field()
    title = scrapy.Field()
    img_url = scrapy.Field()
    tags = scrapy.Field()
    cids = scrapy.Field()


class ChaoxingBook(scrapy.Item):
    ssid = scrapy.Field()
    title = scrapy.Field()
    theme = scrapy.Field()
    comment = scrapy.Field()
    author = scrapy.Field()
    page_count = scrapy.Field()
    publish_time = scrapy.Field()
    publisher = scrapy.Field()
    class_code = scrapy.Field()
    reader_url = scrapy.Field()
    book_type = scrapy.Field()


if __name__ == '__main__':
    item = XinyuBook()
    item['bookid'] = '123'
