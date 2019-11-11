# -*- coding: UTF-8 -*-


import requests
import urlparse
import os
import codecs
from bs4 import BeautifulSoup
import scrapy
from scrapy.selector import Selector
from scrapy.http import HtmlResponse

import re
import json

with open('fuck.html', 'r') as fuck_file:
    f = fuck_file.read()
    jpg_path = re.search(r'var pages = \[.*\];', f).group()[12:-1]

    print jpg_path

    [[a1,b1],[a2,b2],[a3,b3],[a4,b4],[a5,b5],[a6,b6],[a7,b7],[a8,b8]] = json.loads(jpg_path)
    print type(a1)
    for i in range(a1, a1+b1+1):
        print 'cov%.3d'%i
    for i in range(a2, a2+b2):
        print 'bok%.3d'%i
    for i in range(a3, a3+b3):
        print 'leg%.3d'%i
    for i in range(a4, a4+b4):
        print 'fow%.3d'%i
    for i in range(a5, a5+b5):
        print '!%.5d'%i
    # for i in range(a6, a6+b6):
    #     print '%.6d'%i
    for i in range(a7, a7+b7):
        print 'att%.3d'%i
    for i in range(a8, a8+b8-1):
        print 'cov%.3d'%i


    # var pages = [[1, 0], [1, 0], [1, 1], [1, 0], [1, 0], [1, 365], [1, 0], [2, 2]];
    # {v: PAGETYPE.cov, s: 'cov', n: '封面'}, / *封面cov001 * /
    # {v: PAGETYPE.bok, s: 'bok', n: '书名'}, / *书名 * /
    # {v: PAGETYPE.leg, s: 'leg', n: '版权'}, / *版权 * /
    # {v: PAGETYPE.fow, s: 'fow', n: '前言'}, / *前言 * /
    # {v: PAGETYPE.dir, s: '!', n: '目录'}, / *目录 * /
    # {v: PAGETYPE.cnt, s: '', n: '正文'}, / *正文 * /
    # {v: PAGETYPE.att, s: 'att', n: '附录'}, / *附录 * /
    # // {v: PAGETYPE.bac, s: 'bac', n: '封底'} / * 封底 * /
    # {v: PAGETYPE.bac, s: 'cov', n: '封底'} / * 封底cov002 * /

    sb = []
