# -*- coding: UTF-8 -*-

import requests
from bs4 import BeautifulSoup
import scrapy
from scrapy.selector import Selector
from scrapy.http import HtmlResponse


#不想要302重定向直接跳转问题：在get方法里面增加allow_redirects=False
def yiyi_get(url):

    s = requests.Session()
    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.87 Safari/537.36'
    headers = {'User-Agent':user_agent}
    r = s.get(url=url, headers=headers)
    return r

if __name__ == '__main__':
    url = 'http://ffhgfc36ddccdc234f5bb9216d41432f11ddhwn0wvqonnnc66690.fgzi.wap.gxlib.org/book/card?cnFenlei=TS273&ssid=13610233&d=3e7583ba5fb01492eaf243482dcf1690&isFromBW=true'

    book_url = 'http://ffhgfc36ddccdc234f5bb9216d41432f11ddhqwbn0xfqpxuv6wkk.fgzi.wap.gxlib.org/book/card?cnFenlei=TS273&ssid=14424477&d=0e2a9c041ca6a37782e6b74ffb90e993&isFromBW=true&isjgptjs=false'
    book_url2 = 'http://ffhgfc36ddccdc234f5bb9216d41432f11ddhqwbn0xfqpxuv6wkk.fgzi.wap.gxlib.org/book/card?cnFenlei=TS273&ssid=13610233&d=3e7583ba5fb01492eaf243482dcf1690&isFromBW=true&isjgptjs=false'

    # r = yiyi_get(book_url2)
    # span = Selector(response=r).css('span.zli_i_web')[0]
    # print span.css('a::attr(href)').get()

    pdfreader_url = 'http://ffhgfc36ddccdc234f5bb9216d41432f11ddhqwbn0xfqpxuv6wkk.fgzi.wap.gxlib.org/reader/pdf/pdfreader?ssid=96178226&d=791d243c6fd684058ff733a50dd4af24'
    r = yiyi_get(pdfreader_url)
    span = Selector(response=r).css('span.zli_i_web')[0]



    # print type(span)