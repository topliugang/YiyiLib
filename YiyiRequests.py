# -*- coding: UTF-8 -*-
import requests
import urlparse
import os


# 不想要302重定向直接跳转问题：在get方法里面增加allow_redirects=False
# cookie以str传入Yiyirequests类，（暂定）

class YiyiRequests:
    def __init__(self, cookie_str=None):
        self.s = requests.Session()
        user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.87 Safari/537.36'
        self.headers = {'User-Agent': user_agent, }
        # self.cookies = cookies
        if cookie_str:
            self.headers['Cookie'] = cookie_str
            # self.cookies = cookie_str_2_dict(cookies_str)

    def get(self, url):
        # print '### Getting...'
        return self.s.get(url=url, headers=self.headers)

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
            i = i.strip()
            key = i.split('=')[0]
            value = i.split('=')[1]
            cookies[key] = value
    return cookies


# 使用urlparse解析url,获取query参数字典
# 这样获取aaid：aaid = parse_url_parms(url)['aid'][0]
def parse_url_parms(url):
    # url = 'http://sfjulebu.com/forum.php?mod=attachment&aid=Mjk1MDZ8MDI5ZGJlNjJ8MTUyNDUzMTg2OXwyNDQxOXw5Mjc2&nothumb=yes'
    parms_dict = urlparse.parse_qs(urlparse.urlsplit(url).query)
    return parms_dict
