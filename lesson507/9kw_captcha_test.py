#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/2/29 11:07
# @Author  : tanxw
# @Desc    : 9kw api服务  处理复杂的图像验证码处理


import urllib.request
import urllib.parse
import base64
API_URL = 'https://www.9kw.eu/index.cgi'
def send_captcha(api_key, img_data):
    data = {
        'action': 'usercaptchaupload',
        'apikey': api_key,
        'filre-upload-01': base64.b64decode(img_data),
        'base64': '1',
        'selfsolve': '1',
        'maxtimeout': '60'
    }
    encoded_data = urllib.parse.urlencode(data).encode(encoding='utf8')
    request = urllib.request.Request(API_URL, encoded_data)
    response = urllib.request.urlopen(request)
    return response.read()

def get_captcha(api_key, captcha_id):
    data = {
        'action': 'usercaptchacorrectdata',
        'id': captcha_id,
        'apikey': api_key
    }
    encoded_data = urllib.parse.urlencode(data).encode(encoding='utf8')
    # note this is a GET request
    # so the data is appended to the URL
    response = urllib.request.urlopen(API_URL + '?' + encoded_data)
    return response.read()

