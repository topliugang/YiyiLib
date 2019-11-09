# -*- coding: UTF-8 -*-

import requests
import urlparse
import os
import codecs
from bs4 import BeautifulSoup
import scrapy
from scrapy.selector import Selector
from scrapy.http import HtmlResponse
import PyV8
import re


#不想要302重定向直接跳转问题：在get方法里面增加allow_redirects=False
def yiyi_get(url):

    s = requests.Session()
    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.87 Safari/537.36'
    headers = {'User-Agent':user_agent}
    r = s.get(url=url, headers=headers)
    return r

def parse_url_host(url):
    host = urlparse.urlsplit(url).netloc
    ralative_path = os.path.dirname(urlparse.urlsplit(url).path)
    if ralative_path != '/':
        host = host + ralative_path
    return host


def fuck():
    card_url = 'http://ffhgfc36ddccdc234f5bb9216d41432f11ddhoq5pufvqncqv60v6.fgzi.wap.gxlib.org/book/card?cnFenlei=TS273-64&ssid=13677499&d=6f154baf7ec60892601776d79c6cd62a&isFromBW=false&isjgptjs=false'

    r = yiyi_get(card_url)
    span = Selector(response=r).css('span.zli_i_web')[0]
    ahref = span.css('a::attr(href)').get()
    netloc = urlparse.urlparse(card_url).netloc
    scheme = urlparse.urlparse(card_url).scheme

    jpathreader_url = '%s://%s%s'%(scheme,netloc,ahref)
    print jpathreader_url


    r = yiyi_get(jpathreader_url)
    print r.url
    with codecs.open('fuck.html', 'w', encoding='utf-8') as fuck_file:
        fuck_file.write(r.text)
    exit()

if __name__ == '__main__':
    fuck()

    exit()
    html = ''
    with codecs.open('fuck.html', 'r', encoding='utf-8') as fuck_file:
        html = fuck_file.read()

    #selector = Selector(response=r)
    selector = Selector(text=html)

    scripts = selector.css('script')

    print scripts[3].extract()
    js = scripts[3].extract()[8:-9].strip()

    filemark = re.search('var fileMark = "\d*";', js).group()[16:-2]
    #print filemark
    usermark = re.search('var userMark = "\d*";', js).group()[16:-2]
    #print '_'+usermark+'_'


    strr = re.search('DEFAULT_BASE_DOWNLOAD_URL = .+;', js).group()
    #print re.findall("'([^']+)'", strr)
    url = '%s%s%s%s%s'%(re.findall("'([^']+)'", strr)[0],filemark,
                        re.findall("'([^']+)'", strr)[1],usermark,
                        re.findall("'([^']+)'", strr)[2])
    print url


        # with PyV8.JSContext() as ctxt:
        #     ctxt.eval(js)
        #     vars = ctxt.locals
        #     var_ex1 = vars.fileMark
        #     print var_ex1



    # print type(span)