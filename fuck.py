# -*- coding: UTF-8 -*-

# fanqiang https://github.com/bannedbook/fanqiang/wiki/Chrome%E4%B8%80%E9%94%AE%E7%BF%BB%E5%A2%99%E5%8C%85
# http://www.gzlib.org/
# 卡号：GY036423
# 密码：815706
# 需要验证cookies

# http://wap.gxlib.org/ermsClient/browse.do
# 18263735763
# 335762

# 新语授权
# http://jt.wx.xinyulib.com/lib/m/auth/auth.jsp?u=btyxytsgid&a=C3715256C4499F17D849D1A3CCE91746（免登陆密码链接）需复制链接到微信
import sys

reload(sys)
sys.setdefaultencoding('utf8')

import os
import codecs
from bs4 import BeautifulSoup
import scrapy
from scrapy.selector import Selector
from scrapy.http import HtmlResponse
import json
import re
import time
from pyv8 import PyV8
import sqlite3
from PyPDF2 import PdfFileReader, PdfFileWriter
import sqlite3

from YiyiRequests import *
from YiyiSqlite3 import *

sqlite3db = Sqlite3db('./data/db/fuck.db')


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


# 其中的book_type 0:pdf, 1:网页阅读
class Book:
    def __init__(self, ssid, title, theme, comment, author, page_count,
                 publish_time, publisher, class_code, reader_url, book_type):
        self.ssid = ssid
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
        print 'ssid:' + unicode(self.ssid)
        print 'title:' + unicode(self.title)
        print 'theme:' + unicode(self.theme)
        print 'comment:' + unicode(self.comment)
        print 'author:' + unicode(self.author)
        print 'page_count:' + unicode(self.page_count)
        print 'publish_time:' + unicode(self.publish_time)
        print 'publisher:' + unicode(self.publisher)
        print 'class_code:' + unicode(self.class_code)
        print 'reader_url:' + unicode(self.reader_url)
        print 'book_type:' + unicode(self.book_type)


# 解析card页面，返回图书的信息
# 其中的book_type 0:pdf, 1:网页阅读
def parse_card(response):
    selector = Selector(response=response)
    ssid = parse_url_parms(response.url)['ssid'][0]
    title = selector.css('h2.zli_i_h2::text').extract_first()
    theme = selector.css('p.zli_i_tt::text').extract_first()
    comment = selector.css('div.zco_content::text').extract_first()

    author, page_count, publish_time, publisher, class_code = selector.css('li.zli_info p::text').extract()[-5:]

    # 阅读地址
    span = selector.css('span.zli_i_web')[0]
    ahref = span.css('a::attr(href)').get()
    netloc = urlparse.urlparse(response.url).netloc
    scheme = urlparse.urlparse(response.url).scheme
    reader_url = '%s://%s%s' % (scheme, netloc, ahref)
    # 阅读类型
    if 'pdf' in reader_url:
        book_type = 0
    elif 'jpathreader' in reader_url:
        book_type = 1
    book = Book(ssid, title, theme, comment, author, page_count, publish_time,
                publisher, class_code, reader_url, book_type)
    return book


# 根据response生成jpg下载链接，并下载
# 返回一个url_filename_list:[[url,filename],[url,filename]]
def parse_jpath_reader(response):
    jpg_path = re.search('jpgPath: ".+",', response.text).group()[10:-2]
    start_page, end_page = re.search("ps: '\d+-\d+',", response.text).group()[5:-2].split('-')
    start_page = int(start_page)
    end_page = int(end_page)
    netloc = urlparse.urlparse(response.url).netloc
    scheme = urlparse.urlparse(response.url).scheme

    [[a1, b1], [a2, b2], [a3, b3], [a4, b4], [a5, b5], [a6, b6], [a7, b7], [a8, b8]] = json.loads(
        re.search(r'var pages = \[.*\];', response.text).group()[12:-1])
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

    index = 0
    url_filename_list = []
    for jpg_code in jpg_codes:
        url = jpg_url_template % (jpg_code)
        pre_filename = '%.6d' % index
        filename = '%s_%s.jpg' % (pre_filename, jpg_code)
        index = index + 1
        url_filename_list.append([url, filename])
        # yiyi_request.download(url, './jpg/%s.jpg' % jpg_code)
    return url_filename_list


# 根据response生成pdf下载链接，下载
# 返回一个url_filename_list:[[url,filename],[url,filename]]
def parse_pdf_reader(response):
    selector = Selector(response=response)
    js = selector.css('script')[3].extract()[8:-9].strip()
    filemark = re.search('var fileMark = "\d*";', js).group()[16:-2]
    usermark = re.search('var userMark = "\d*";', js).group()[16:-2]
    pagecount = re.search('var total = \d+;', js).group()[12:-1]
    filename = re.search('var fileName = ".*";', js).group()[16:-2]
    # print filemark
    base_download_url = re.search('DEFAULT_BASE_DOWNLOAD_URL = .+;', js).group()
    # print re.findall("'([^']+)'", base_download_url)
    pdf_url_template = '%s%s%s%s%s' % (re.findall("'([^']+)'", base_download_url)[0], filemark,
                                       re.findall("'([^']+)'", base_download_url)[1], usermark,
                                       re.findall("'([^']+)'", base_download_url)[2])

    url_filename_list = []
    for i in range(1, int(pagecount) + 1):
        pdf_page_url = '%s&cpage=%d' % (pdf_url_template, i)
        filename = '%.6d.pdf' % i
        url_filename_list.append([pdf_page_url, filename])
        # filepath = os.path.join(temp_pdf_path, '%d.pdf' % i)
        # # print 'Download %s...'%filepath
        # yiyi_request.download(pdf_page_url, filepath)
    return url_filename_list

    # #这一部分是关于文件夹操作，先清空temp文件夹，再合并pdf
    # #需要修改
    # temp_pdf_path = './temp'
    # # 清空temp文件夹
    # for filename in os.listdir(temp_pdf_path):
    #     fullpath = os.path.join(temp_pdf_path, filename)
    #     os.remove(fullpath)
    #
    # pdf_paths = []
    # for i in range(1, int(pagecount) + 1):
    #     pdf_paths.append(os.path.join(temp_pdf_path, '%d.pdf' % i))
    #
    # hebingpdf(pdf_paths, '%s.pdf' % filename)


# 逻辑：
# 1.访问card页面，生成Book信息
# 2.访问Book中的reader_url页面，生成下载链接
def fuck(card_url, cookie_str=None):
    yiyi_request = YiyiRequests(cookie_str=cookie_str)
    r = yiyi_request.get(card_url)
    book = parse_card(r)
    print '### Book parsed.'
    print '###   Name:%s' % book.title.replace(u'\xa0', u'')
    print '###   Ssid:%s' % book.ssid
    print '###   Page_count:%s' % book.page_count

    if book.book_type == 0:  # pdf
        r = yiyi_request.get(book.reader_url)
        url_filename_list = parse_pdf_reader(r)
    elif book.book_type == 1:  # 网页阅读
        r = yiyi_request.get(book.reader_url)
        url_filename_list = parse_jpath_reader(r)

    book_dir = './%s' % (book.ssid)
    if os.path.exists(book_dir):
        print '### Already exists dir:%s,exit.' % book_dir
        exit()
    os.mkdir(book_dir)
    print '### Dir created: %s.' % book_dir

    for url, filename in url_filename_list:
        filepath = os.path.join(book_dir, filename)
        yiyi_request.download(url, filepath)
        time.sleep(1)


class XinyuBook:
    def __init__(self, bookid, detail_url, full_detail_url, title, img_url, tags, cids):
        self.bookid = bookid
        self.detail_url = detail_url
        self.full_detail_url = full_detail_url
        self.title = title
        self.img_url = img_url
        self.tags = tags
        self.cids = cids

    @classmethod
    def create_table(cls):
        create_table_sql = """drop table if exists xinyu_book;
                            create table xinyu_book(
                            book_id text,
                            detail_url text,
                            full_detail_url text,
                            title text,
                            img_url text,
                            tags text,
                            cids text,
                            primary key(book_id)
                            );"""
        con = sqlite3.connect('./data/db/fuck.db')
        cur = con.cursor()
        sql_template = create_table_sql
        # cur.executescript(sql_template.format(db_names[0], db_names[1], db_names[2]))
        cur.executescript(sql_template)
        con.commit()
        con.close()

    def insrt(self):
        sql = 'insert or replace into xinyu_book(book_id,detail_url,full_detail_url,title,img_url,tags,cids)' \
              'values(?,?,?,?,?,?,?)'
        values = [self.bookid, self.detail_url, self.full_detail_url, self.title, self.img_url, json.dumps(self.tags),
                  json.dumps(self.cids)]
        sqlite3db.get_coon().execute(sql, values)
        sqlite3db.commit()
        print '### insert OK!    %s' % self.title


def xinyu_audio_servlet_url(bookid, cid, stype):
    with PyV8.JSContext() as ctxt:
        js = open('utils.js', 'r').read()
        ctxt.locals.bookid = bookid
        ctxt.locals.cid = cid
        ctxt.locals.stype = ''
        ctxt.eval(js)
        return ctxt.locals.audio_servlet_url


# 测试ac加密
def fuck(input):
    with PyV8.JSContext() as ctxt:
        js = open('utils.js', 'r').read()
        ctxt.locals.bookid = ''
        ctxt.locals.cid = ''
        ctxt.locals.stype = ''
        ctxt.locals.input = input
        ctxt.eval(js)
        return ctxt.locals.fuck


def parse_morepage(r):
    selector = Selector(response=r)
    xinyuBooks = []
    divs = selector.css('div.course')
    for div in divs:
        detail_url = div.css('a::attr(href)').extract_first()
        bookid = parse_url_parms(detail_url)['bookid'][0]
        title = div.css('div.title::text').extract_first()
        img_url = re.search(r'url\(.+\);', div.css('div.imgDiv::attr(style)').extract_first()).group()[4:-2]
        tags = []
        for tag in div.css('div.text::text').extract():
            tags.append(tag)

        after_url = os.path.abspath(os.path.join(os.path.dirname(urlparse.urlsplit(r.url).path), detail_url))

        netloc = urlparse.urlparse(r.url).netloc
        scheme = urlparse.urlparse(r.url).scheme
        full_detail_url = '%s://%s%s' % (scheme, netloc, after_url)

        xinyuBook = XinyuBook(bookid, detail_url, full_detail_url, title, img_url, tags, None)
        xinyuBooks.append(xinyuBook)
    return xinyuBooks


def parse_detail(r):
    detail_selector = Selector(response=r)
    cids = detail_selector.css('div.weui-cell::attr(id)').extract()
    return cids


def fuck_xinyu():
    index_url = 'http://jt.wx.xinyulib.com.cn/lib/m/index/'
    cookie_str = 'JSESSIONID=B2E73F17B7EEF13DC78229FAE26084B1; state=R9ZA47SK0TMX3Z9CHGHA4JWDA4LQNZDB; xinyu="eyJ1bmFtZSI6IuWMheWktOWMu+WtpumZoiIsInd4ZG9tIjoianQud3gueGlueXVsaWIuY29tLmNuIiwiaXNzaGFyZSI6IjAiLCJ1dHlwZSI6IjAiLCJ0aXRsZSI6IuaWsOivreaVsOWtl+WbvuS5pummhiIsInBhY2siOiJsaWIiLCJ1c2VyaWQiOiI3NzUiLCJzaG93bmFtZSI6IiIsImVib29rIjoiMSIsInBjZG9tIjoianQueGlueXVsaWIuY29tLmNuIiwic2l0ZWlkIjoiMzUiLCJ1bml0aWQiOiIyNzIiLCJsb2dvIjoiIn0="; pubxinyu="eyJzaG93bmFtZSI6IiIsInVuYW1lIjoi5YyF5aS05Yy75a2m6ZmiIiwid3hkb20iOiJqdC53eC54aW55dWxpYi5jb20uY24iLCJwY2RvbSI6Imp0Lnhpbnl1bGliLmNvbS5jbiIsInNpdGVpZCI6IjM1IiwidW5pdGlkIjoiMjcyIiwidGl0bGUiOiLmlrDor63mlbDlrZflm77kuabppoYiLCJwYWNrIjoibGliIn0="'
    morepage_url_template = 'http://jt.wx.xinyulib.com.cn/lib/m/search/more.jsp?sw=%%EF%%BC%%8C&page=%d'
    morepage_url_template = 'http://jt.wx.xinyulib.com.cn/lib/m/search/more.jsp?classid=866&page=%d'
    yiyi_request = YiyiRequests(cookie_str=cookie_str)

    for i in range(1, 150):
        print '### PAGE---------%d'%i
        morepage_url = morepage_url_template % i
        r = yiyi_request.get(morepage_url)
        xinyuBooks = parse_morepage(r)
        for xinyuBook in xinyuBooks:
            r1 = yiyi_request.get(xinyuBook.full_detail_url)
            cids = parse_detail(r1)
            xinyuBook.cids = json.dumps(cids)
            xinyuBook.insrt()
        time.sleep(1)

    # for cid in cids:
    #     audio_servlet_url = xinyu_audio_servlet_url(bookid, cid, '')
    #     full_audio_servlet_url = '%s://%s%s' % (scheme, netloc, audio_servlet_url)
    #     print full_audio_servlet_url
    #
    #     mp3_url = yiyi_request.get(full_audio_servlet_url).text
    #     yiyi_request.download(mp3_url, 'fuck.mp3')


if __name__ == '__main__':
    # XinyuBook.create_table()

    # card_url = 'http://www.sslibrary.com/book/card?ssid=96136883&d=ea4be8af9f69453d07c594e4933a0da7&cnFenlei=F276.5&dxid=000016584446&isFromBW=true '
    # cookie_str = 'loginType=certify; username=gzsztsg; account=GY036423; deptid=1078; msign=105132512894418; enc=8e6e4a9eda70155820cf591e084de958; DSSTASH_LOG=C%5f34%2dUN%5f1078%2dUS%5f%2d1%2dT%5f1573472518774; UM_distinctid=16e5a4613ab2ef-060a546b625c3b-1c3c6a5a-13c680-16e5a4613acdb; route=a43339488179d54bb7f54cfa4036b6de; JSESSIONID=5628ABD4020465AA6A2778ACFF7C289C.dsk45_web; ruot=1573489719665'
    card_url = 'http://ffhgfc36ddccdc234f5bb9216d41432f11ddhnco0c65fqbp56vo9.fgzi.wap.gxlib.org/book/card?cnFenlei=G899&ssid=11340863&d=cf93ed466df541d847db2f489ca9e264&isFromBW=false&isjgptjs=false'
    cookie_str = 'UM_distinctid=16e341868f8159-002e753a3731f5-5d1f3b1c-1fa400-16e341868f95d4; CWJSESSIONID=B89CE9531962B064C05E135F2A1FA25C; cwsid=e87b845a12954f76'
    # fuck(card_url, cookie_str=cookie_str)

    fuck_xinyu()

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

    # print type(span)
