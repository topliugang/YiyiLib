# -*- coding: UTF-8 -*-
import requests
import urlparse
import os
import random


# 不想要302重定向直接跳转问题：在get方法里面增加allow_redirects=False
# cookie以str传入Yiyirequests类，（暂定）
#用法：yiyiRequests = YiyiRequest()
# yiyiRequests.get(url)
# YiyiRequest.get_random_ua()
class YiyiRequests:
    def __init__(self, cookie_str=None):
        self.s = requests.Session()
        user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.87 Safari/537.36'
        self.headers = {'User-Agent': user_agent, }
        # self.cookies = cookies
        if cookie_str:
            self.headers['Cookie'] = cookie_str
            # self.cookies = cookie_str_2_dict(cookies_str)

    def get(self, url, proxies=None, timeout=None):
        # print '### Getting...'
        return self.s.get(url=url, headers=self.headers, proxies=proxies, timeout=timeout)

    def download(self, url, path):
        print '### Downloading...'
        r = self.get(url)
        with open(path, 'wb') as downloadfile:
            downloadfile.write(r.content)

    @classmethod
    def parse_url_host(cls, url):
        host = urlparse.urlsplit(url).netloc
        ralative_path = os.path.dirname(urlparse.urlsplit(url).path)
        if ralative_path != '/':
            host = host + ralative_path
        return host

    @classmethod
    def cookie_str_2_dict(cls, cookie_str):
        cookies = {}
        if ';' in cookie_str:
            for i in cookie_str.split(';'):
                i = i.strip()
                key = i.split('=')[0]
                value = i.split('=')[1]
                cookies[key] = value
        return cookies

    # 使用urlparse解析url,获取query参数字典
    # 这样获取aaid：aaid = parse_url_parms(url)['aid'][0]
    @classmethod
    def parse_url_parms(cls, url):
        # url = 'http://sfjulebu.com/forum.php?mod=attachment&aid=Mjk1MDZ8MDI5ZGJlNjJ8MTUyNDUzMTg2OXwyNDQxOXw5Mjc2&nothumb=yes'
        parms_dict = urlparse.parse_qs(urlparse.urlsplit(url).query)
        return parms_dict

    @classmethod
    def get_random_ua(cls):
        user_agent_list = [ \
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1" \
            "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11", \
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6", \
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6", \
            "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1", \
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5", \
            "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5", \
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3", \
            "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3", \
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3", \
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3", \
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3", \
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3", \
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3", \
            "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3", \
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3", \
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24", \
            "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
        ]
        return random.choice(user_agent_list)
