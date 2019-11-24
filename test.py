# -*- coding: UTF-8 -*-


from items import XinyuBook, item_select, item_insert, item_create_table, item_update
import json
import re

if __name__ == '__main__':
    # item_create_table(XinyuBook)
    # item_insert(item)
    items = item_select(XinyuBook)
    for item in items:
        print json.loads(item['cids'])
        exit()
