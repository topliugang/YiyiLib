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


class YiyiFileItem(scrapy.Item):
    file_path = None
    filename = scrapy.Field()


class XinyuBook(YiyiItem):
    book_id = scrapy.Field()
    detail_url = scrapy.Field()
    full_detail_url = scrapy.Field()
    title = scrapy.Field()
    img_url = scrapy.Field()
    tags = scrapy.Field()
    cids = scrapy.Field()
    table_name = 'xinyu_book'


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

class ProxyItem(YiyiItem):
    ip = scrapy.Field()
    port = scrapy.Field()
    niming = scrapy.Field()
    type = scrapy.Field()
    site = scrapy.Field()
    table_name = 'proxy'


# 获取指定item的数据，传入的为item类名
def item_select(YiyiItemClassName, sql=None):
    yiyiItems = []
    if not sql:
        sql = 'select * from %s ' % YiyiItemClassName.table_name
    for row in sqlite3db.select(sql):
        yiyiItem = YiyiItemClassName()
        for col_name in row.keys():
            yiyiItem[col_name] = row[col_name]
        yiyiItems.append(yiyiItem)
    return yiyiItems


def item_create_table(YiyiItemClassName):
    field_list = []
    for field in YiyiItemClassName.fields:
        field_list.append('%s text' % field)
    field_str = ','.join(field_list)
    create_table_sql = 'drop table if exists {0};create table {0}({1});'.format(YiyiItemClassName.table_name, field_str)
    sqlite3db.create_table(create_table_sql)


def item_insert(yiyiItem):
    # sqlite3db.execute()
    insert_sql = "insert into {0}({1}) values ({2})".format(yiyiItem.table_name,
                                                            ', '.join(yiyiItem.fields),
                                                            ', '.join(['?'] * len(yiyiItem.fields)))
    # item.key()  item.values()取key 和value
    values = [yiyiItem[db_columen] for db_columen in yiyiItem.fields]
    sqlite3db.execute(insert_sql, values)


def item_update(yiyiItem, key):
    field_list = []
    for field in yiyiItem.fields:
        field_list.append('%s=?' % field)
    field_str = ','.join(field_list)
    update_sql = 'update {0} set {1} where {2}={3}'.format(yiyiItem.table_name, field_str, key, '?')
    values = [yiyiItem[db_columen] for db_columen in yiyiItem.fields]
    values.append(yiyiItem[key])

    sqlite3db.execute(update_sql, values)


if __name__ == '__main__':
    # print type(XinyuBook)
    # sb = XinyuBook.select()
    items = item_select(XinyuBook)
    # print items[1]
    item_insert(items[1])
