#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/2/28 23:16
# @Author  : tanxw
# @Desc    : 自动化注册-验证码处理

from http import cookiejar
import urllib.request
import pprint
from lesson506 import login

REGISTER_URL = 'http://example.webscraping.com/places/default/user/register'
cj = cookiejar.CookieJar()
cookie_handler = urllib.request.HTTPCookieProcessor(cj)
opener = urllib.request.build_opener(cookie_handler)
html = opener.open(REGISTER_URL).read()
form = login.parse_form(html)
pprint.pprint(form)

from io import BytesIO
import lxml.html
from PIL import Image
import base64
def get_captcha(html):
    tree = lxml.html.fromstring(html.decode('utf8'))
    img_data = tree.cssselect('div#recaptcha img')[0].get('src')
    img_data = img_data.partition(',')[-1]
    binary_img_data = base64.b64decode(img_data)
    file_like = BytesIO(binary_img_data)
    img = Image.open(file_like)
    return img

import pytesseract

img = get_captcha(html)
pytesseract.image_to_string(img)