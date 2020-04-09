#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/2/28 21:55
# @Author  : tanxw
# @Desc    : jd - login

# 使用win32crypt功能
# pip install pypiwin32

import sqlite3
from http import cookiejar
import urllib.request
import urllib.parse
import os,sys
import win32crypt


def build_opener_with_chrome_cookies(domain=None):
    cookie_file_path = os.path.join(os.environ['LOCALAPPDATA'], r'Google\Chrome\User Data\Default\Cookies')
    if not os.path.exists(cookie_file_path):
        raise Exception('Cookies file not exist!')
    conn = sqlite3.connect(cookie_file_path)
    # sql = 'select host_key, name, value, path from cookies'
    sql = "select host_key,name,encrypted_value,path from cookies"
    if domain:
        sql += ' where host_key like "%{}%"'.format(domain)

    cj = cookiejar.CookieJar()  # No cookies stored yet

    for row in conn.execute(sql):
        pwdHash = str(row[2])
        try:
            ret = win32crypt.CryptUnprotectData(pwdHash, None, None, None, 0)
        except:
            print('Fail to decrypt chrome cookies')
            sys.exit(-1)

        cookie_item = cj.Cookie(
            version=0, name=row[1], value=ret[1],
            port=None, port_specified=None,
            domain=row[0], domain_specified=None, domain_initial_dot=None,
            path=row[3], path_specified=None,
            secure=None,
            expires=None,
            discard=None,
            comment=None,
            comment_url=None,
            rest=None,
            rfc2109=False,
        )
        cookiejar.set_cookie(cookie_item)  # Apply each cookie_item to cookiejar
    conn.close()

    proxy = {'http': '27.24.163.155:10'}
    return urllib.request.build_opener(urllib.request.ProxyHandler(proxy),
                                       urllib.request.HTTPCookieProcessor(cookiejar))


if __name__ == '__main__':
    opener = build_opener_with_chrome_cookies(domain='jd.com')
    headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:48.0) Gecko/20100101 Firefox/48.0",'Referer': 'https://www.jd.com/'}
    url='https://order.jd.com/center/list.action'
    req = urllib.request.Request(url, headers=headers)
    response = opener.open(req)
    print(response)