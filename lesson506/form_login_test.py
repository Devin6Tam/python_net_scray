#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/2/28 17:46
# @Author  : tanxw
# @Desc    : 表单登录交互

import urllib.request
import urllib.parse
login_url = 'http://example.webscraping.com/places/default/user/login'
login_email = 'txtxw@163.com'
login_password = 'a123456'

# data = {'email': login_email, 'password': login_password}
# encode_data = urllib.parse.urlencode(data).encode(encoding='utf-8')
# request = urllib.request.Request(login_url, encode_data)
# response = urllib.request.urlopen(request)
# print(response.geturl())
#
#
import lxml.html
def parse_form(html):
    tree = lxml.html.fromstring(html)
    data = {}
    for e in tree.cssselect('form input'):
        if e.get('name'):
            data[e.get('name')] = e.get('value')
    return data
#
import pprint
# html = urllib.request.urlopen(login_url).read()
# data = parse_form(html)
# pprint.pprint(data)
# data['email'] = login_email
# data['password'] = login_password
# encode_data = urllib.parse.urlencode(data).encode(encoding='utf-8')
# request = urllib.request.Request(login_url, encode_data)
# response = urllib.request.urlopen(request)
# print(response.geturl())

# 支持firefox浏览器cookie使用，如需要使用其他浏览器的cookie，需要安装pip install browsercookie
from http import cookiejar
cj = cookiejar.CookieJar()
# opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
cookie_handler = urllib.request.HTTPCookieProcessor(cj)
opener = urllib.request.build_opener(cookie_handler)

opener.addhandlers = [("User-Agent", "Opera/9.80 (Windows NT 6.1; U; zh-cn) Presto/2.9.168 Version/11.50")]
html = opener.open(login_url).read()
data = parse_form(html)
data['email'] = login_email
data['password'] = login_password
encode_data = urllib.parse.urlencode(data).encode(encoding='utf-8')
request = urllib.request.Request(login_url, encode_data)
response = opener.open(request)
print(response.geturl())

