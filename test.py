# -*- coding: UTF-8 -*-

import json
import re
import time
from items import XinyuBook, ProxyItem, item_select, item_insert, item_create_table, item_update

from YiyiRequests import YiyiRequests
from scrapy.selector import Selector


def test_xinyubook():
    # item_create_table(XinyuBook)
    # item_insert(item)
    items = item_select(XinyuBook)
    for item in items:
        print json.loads(item['cids'])
        exit()


def parse_xici(r):
    selector = Selector(response=r)
    ip_list = selector.css('#ip_list')
    items = []
    for tr in ip_list.css('tr')[1:]:
        tds = tr.css('td')
        item = ProxyItem()
        item['ip'] = tds[1].css("td::text").extract_first()
        item['port'] = tds[2].css("td::text").extract_first()
        item['niming'] = tds[4].css("td::text").extract_first()
        item['type'] = tds[5].css("td::text").extract_first()
        item['site'] = 'xici'
        items.append(item)
    return items


def fuck_proxy():
    yiyi_request = YiyiRequests()
    url_tempate = 'https://www.xicidaili.com/nn/%d'
    for i in range(1, 7):
        url = url_tempate % i
        items = parse_xici(yiyi_request.get(url))
        for item in items:
            item_insert(item)
        time.sleep(5)


def check_proxy():
    items = item_select(ProxyItem)
    yiyi_request = YiyiRequests()
    for item in items[0:5]:
        print item
        ip = item['ip']
        port = item['port']
        scheme = item['type']
        check_url = scheme + '://httpbin.org/ip'
        check_url = scheme + '://www.google.com'
        check_url = scheme + '://www.baidu.com'
        proxy = scheme + '://' + ip + ':' + port
        meta = {
            'proxy': proxy,
            'dont_retry': True,
            'download_timeout': 30,
            'item': item,
        }
        proxies = {'http': proxy, 'https': proxy}
        print '### Checking proxy: "%s"' % proxy
        try:
            r = yiyi_request.get(url=check_url, proxies=proxies,timeout=5)
            print r.status_code
        except Exception as e:
            print e



def test_proxy():
    # item_create_table(ProxyItem)
    check_proxy()


if __name__ == '__main__':
    test_proxy()
