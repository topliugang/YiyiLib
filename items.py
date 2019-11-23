# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from YiyiSqlite3 import sqlite3db


# 原则：数据全部为字符串，list，dict等转换成json字符串

class YiyiItem(scrapy.Item):
    table_name = None

    def create_table(self):
        for sb in self.fields:
            print sb

    @classmethod
    def select(cls):
        print dir(cls)
        yiyiItems = []
        for row in sqlite3db.select('select * from %s limit 10 ' % cls.table_name):
            yiyiItem = cls.__init__()
            print yiyiItem

            exit()
            for col_names in row.keys():
                # print col_names
                yiyiItem[col_names] = row[col_names]
            yiyiItems.append(yiyiItem)
        return yiyiItems


# select insert update delete
class XinyuBook(YiyiItem):
    book_id = scrapy.Field()
    detail_url = scrapy.Field()
    full_detail_url = scrapy.Field()
    title = scrapy.Field()
    img_url = scrapy.Field()
    tags = scrapy.Field()
    cids = scrapy.Field()
    table_name = 'xinyu_book'

    # @classmethod
    # def select(cls):
    #     xinyuBooks = []
    #     for row in sqlite3db.select('select * from xinyu_book limit 10 '):
    #         xinyuBook = XinyuBook()
    #         for col_names in row.keys():
    #             # print col_names
    #             xinyuBook[col_names] = row[col_names]
    #         xinyuBooks.append(xinyuBook)
    #     return xinyuBooks


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
    sb = XinyuBook.select()

