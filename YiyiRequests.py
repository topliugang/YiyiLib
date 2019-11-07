# -*- coding: UTF-8 -*-

import requests
from bs4 import BeautifulSoup
import scrapy
from scrapy.selector import Selector
from scrapy.http import HtmlResponse

def yiyi_get(url):

    s = requests.Session()
    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.87 Safari/537.36'
    headers = {'User-Agent':user_agent}
    r = s.get(url=url, headers=headers)
    return r

if __name__ == '__main__':
    url = 'http://ffhgfc36ddccdc234f5bb9216d41432f11ddhwn0wvqonnnc66690.fgzi.wap.gxlib.org/book/card?cnFenlei=TS273&ssid=13610233&d=3e7583ba5fb01492eaf243482dcf1690&isFromBW=true'
    r = yiyi_get(url)
    span = Selector(response=r).css('span.zli_i_web')[0]
    print span.css('a::attr(href)').get()
    # print type(span)