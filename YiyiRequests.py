# -*- coding: UTF-8 -*-
#http://www.gzlib.org/
# 卡号：GY036423
# 密码：815706
#需要验证cookies

# http://wap.gxlib.org/ermsClient/browse.do
# 18263735763
# 335762


import requests
import urlparse
import os
import codecs
from bs4 import BeautifulSoup
import scrapy
from scrapy.selector import Selector
from scrapy.http import HtmlResponse
import json
import re

from PyPDF2 import PdfFileReader, PdfFileWriter


# 不想要302重定向直接跳转问题：在get方法里面增加allow_redirects=False
class YiyiRequests:
    def __init__(self, cookies=None):
        self.s = requests.Session()
        user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.87 Safari/537.36'
        self.headers = {'User-Agent': user_agent}
        self.cookies = cookies


    def get(self, url):
        # print '### Getting...'
        return self.s.get(url=url, headers=self.headers,cookies=self.cookies)

    def download(self, url, path):
        print '### Downloading...'
        r = self.get(url)
        with open(path, 'wb') as downloadfile:
            downloadfile.write(r.content)


def parse_url_host(url):
    host = urlparse.urlsplit(url).netloc
    ralative_path = os.path.dirname(urlparse.urlsplit(url).path)
    if ralative_path != '/':
        host = host + ralative_path
    return host

def cookie_str_2_dict(cookie_str):
    cookies = {}
    if ';' in cookie_str:
        for i in cookie_str.split(';'):
            key = i.split('=')[0]
            value = i.split('=')[1]
            cookies[key] = value
    return cookies

def fuck(card_url):
    temp_pdf_path = './temp'
    # 清空temp文件夹
    for filename in os.listdir(temp_pdf_path):
        fullpath = os.path.join(temp_pdf_path, filename)
        os.remove(fullpath)
    # card页面
    yiyi_request = YiyiRequests()
    # card_url = 'http://ffhgfc36ddccdc234f5bb9216d41432f11ddhfknpu959v5uo6fb9.fgzi.wap.gxlib.org/book/card?cnFenlei=TS273&ssid=14424477&d=0e2a9c041ca6a37782e6b74ffb90e993&isFromBW=true&isjgptjs=false'
    r = yiyi_request.get(card_url)
    span = Selector(response=r).css('span.zli_i_web')[0]
    ahref = span.css('a::attr(href)').get()
    netloc = urlparse.urlparse(card_url).netloc
    scheme = urlparse.urlparse(card_url).scheme
    # 取得pdf阅读按钮的完全地址
    jpathreader_url = '%s://%s%s' % (scheme, netloc, ahref)
    r = yiyi_request.get(jpathreader_url)

    selector = Selector(response=r)
    js = selector.css('script')[3].extract()[8:-9].strip()
    filemark = re.search('var fileMark = "\d*";', js).group()[16:-2]
    usermark = re.search('var userMark = "\d*";', js).group()[16:-2]
    pagecount = re.search('var total = \d+;', js).group()[12:-1]
    filename = re.search('var fileName = ".*";', js).group()[16:-2]
    # print filename
    base_download_url = re.search('DEFAULT_BASE_DOWNLOAD_URL = .+;', js).group()
    # print re.findall("'([^']+)'", base_download_url)
    pdf_url_template = '%s%s%s%s%s' % (re.findall("'([^']+)'", base_download_url)[0], filemark,
                                       re.findall("'([^']+)'", base_download_url)[1], usermark,
                                       re.findall("'([^']+)'", base_download_url)[2])

    for i in range(1, int(pagecount) + 1):
        pdf_page_url = '%s&cpage=%d' % (pdf_url_template, i)
        filepath = os.path.join(temp_pdf_path, '%d.pdf' % i)
        # print 'Download %s...'%filepath
        yiyi_request.download(pdf_page_url, filepath)

    pdf_paths = []
    for i in range(1, int(pagecount) + 1):
        pdf_paths.append(os.path.join(temp_pdf_path, '%d.pdf' % i))

    hebingpdf(pdf_paths, '%s.pdf' % filename)


def hebingpdf(input_paths, output_path):
    print '### PDF hebinging...'
    output = PdfFileWriter()
    outputPages = 0
    for input_path in input_paths:
        # print '--- %s'%input_path
        input = PdfFileReader(open(input_path, 'rb'))
        pageCount = input.getNumPages()
        outputPages += pageCount
        for i in range(pageCount):
            output.addPage(input.getPage(i))
    with open(output_path, "wb") as output_file:
        output.write(output_file)
    print("### PDF hebing completed!")


def fuck2(card_url):
    yiyi_request = YiyiRequests()
    # card_url = 'http://ffhgfc36ddccdc234f5bb9216d41432f11ddhfknpu959v5uo6fb9.fgzi.wap.gxlib.org/book/card?cnFenlei=TS273&ssid=14424477&d=0e2a9c041ca6a37782e6b74ffb90e993&isFromBW=true&isjgptjs=false'
    r = yiyi_request.get(card_url)
    span = Selector(response=r).css('span.zli_i_web')[0]
    ahref = span.css('a::attr(href)').get()
    netloc = urlparse.urlparse(card_url).netloc
    scheme = urlparse.urlparse(card_url).scheme
    # 取得pdf阅读按钮的完全地址
    jpathreader_url = '%s://%s%s' % (scheme, netloc, ahref)
    # print jpathreader_url
    r = yiyi_request.get(jpathreader_url)
    # with codecs.open('fuck.html', 'w', encoding='utf-8') as fuck_file:
    #     fuck_file.write(r.text)
    # selector = Selector(response=r)
    jpg_path = re.search('jpgPath: ".+",', r.text).group()[10:-2]
    start_page, end_page = re.search("ps: '\d+-\d+',", r.text).group()[5:-2].split('-')
    start_page = int(start_page)
    end_page = int(end_page)
    netloc = urlparse.urlparse(r.url).netloc
    scheme = urlparse.urlparse(r.url).scheme

    [[a1, b1], [a2, b2], [a3, b3], [a4, b4], [a5, b5], [a6, b6], [a7, b7], [a8, b8]] = json.loads(
        re.search(r'var pages = \[.*\];', r.text).group()[12:-1])
    jpg_codes = []
    for i in range(a1, a1 + b1 + 1):
        jpg_codes.append('cov%.3d' % i)
    for i in range(a2, a2 + b2):
        jpg_codes.append('bok%.3d' % i)
    for i in range(a3, a3 + b3):
        jpg_codes.append('leg%.3d' % i)
    for i in range(a4, a4 + b4):
        jpg_codes.append('fow%.3d' % i)
    for i in range(a5, a5 + b5):
        jpg_codes.append('!%.5d' % i)
    for i in range(a6, a6 + b6):
        jpg_codes.append('%.6d' % i)
    for i in range(a7, a7 + b7):
        jpg_codes.append('att%.3d' % i)
    for i in range(a8, a8 + b8 - 1):
        jpg_codes.append('cov%.3d' % i)

    jpg_url_template = '%s://%s%s%%s?zoom=2' % (scheme, netloc, jpg_path)
    print jpg_url_template

    for jpg_code in jpg_codes:
        url = jpg_url_template % (jpg_code)
        yiyi_request.download(url, './jpg/%s.jpg' % jpg_code)



#其中的book_type 0:pdf, 1:网页阅读
class Book:
    def __init__(self, title, theme, comment, author, page_count,
                 publish_time, publisher, class_code, reader_url, book_type):
        self.title = title
        self.theme = theme
        self.comment = comment
        self.author = author
        self.page_count = page_count
        self.publish_time = publish_time
        self.publisher = publisher
        self.class_code = class_code
        self.reader_url = reader_url
        self.book_type = book_type

    def print_me(self):
        print self.title
        print self.theme
        print self.comment
        print self.author
        print self.page_count
        print self.publish_time
        print self.publisher
        print self.class_code
        print self.reader_url
        print self.book_type


#解析card页面，返回图书的信息
#其中的book_type 0:pdf, 1:网页阅读
def parse_card(response):
    selector = Selector(response=response)
    title = selector.css('h2.zli_i_h2::text').extract_first()
    theme = selector.css('p.zli_i_tt::text').extract_first()
    comment = selector.css('div.zco_content::text').extract_first()
    author, page_count, publish_time, publisher, class_code = selector.css('li.zli_info p::text').extract()[1:]
    #阅读地址
    span = selector.css('span.zli_i_web')[0]
    ahref = span.css('a::attr(href)').get()
    netloc = urlparse.urlparse(response.url).netloc
    scheme = urlparse.urlparse(response.url).scheme
    reader_url = '%s://%s%s' % (scheme, netloc, ahref)
    #阅读类型
    if 'pdf' in reader_url:
        book_type = 0
    elif 'jpathreader' in reader_url:
        book_type = 1
    book = Book(title, theme, comment, author, page_count, publish_time,
                publisher, class_code, reader_url, book_type)
    return book


if __name__ == '__main__':
    # fuck('http://ffhgfc36ddccdc234f5bb9216d41432f11ddh6vk9unuobxw56n69.fgzi.wap.gxlib.org/book/card?cnFenlei=A841.68&ssid=13680758&d=bd2d9b7e4b4d6a2861e036bc492e7bdf&isFromBW=true&isjgptjs=false')
    # fuck2('http://ffhgfc36ddccdc234f5bb9216d41432f11ddhxfufxnoubbfb6kon.fgzi.wap.gxlib.org/book/card?cnFenlei=TS273&ssid=13044240&d=79b72251f15ad256652e6b831874bb90&isFromBW=false&isjgptjs=false')
    # input = PdfFileReader(open('./temp/4.pdf', 'rb'))
    card_url = 'http://www.sslibrary.com/book/card?cnFenlei=J952&ssid=13474579&d=bbe6937a0a4eb9e145b33cc8238ec6cb&isFromBW=false&isjgptjs=false'
    cookie_str = 'loginType=certify; username=gzsztsg; account=GY036423; deptid=1078; msign=105132512894418; enc=8e6e4a9eda70155820cf591e084de958; DSSTASH_LOG=C%5f34%2dUN%5f1078%2dUS%5f%2d1%2dT%5f1573472518774; UM_distinctid=16e5a4613ab2ef-060a546b625c3b-1c3c6a5a-13c680-16e5a4613acdb; route=a43339488179d54bb7f54cfa4036b6de; JSESSIONID=5628ABD4020465AA6A2778ACFF7C289C.dsk45_web; ruot=1573489719665'
    yiyi_request = YiyiRequests(cookie_str_2_dict(cookie_str))
    r = yiyi_request.get(card_url)
    book = parse_card(r)
    book.print_me()


    exit()

    pdf_paths = []
    temp_pdf_path = './temp'
    for i in range(1, 97):
        pdf_paths.append(os.path.join(temp_pdf_path, '%d.pdf' % i))

    hebingpdf(pdf_paths, '%s.pdf' % '爱上一杯拉花咖啡')

    exit()
    html = ''
    with codecs.open('fuck.html', 'r', encoding='utf-8') as fuck_file:
        html = fuck_file.read()

    # with PyV8.JSContext() as ctxt:
    #     ctxt.eval(js)
    #     vars = ctxt.locals
    #     var_ex1 = vars.fileMark
    #     print var_ex1

    # print type(span)
