#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/2/28 19:10
# @Author  : tanxw
# @Desc    : 表单登录

# -*- coding: utf-8 -*-


import urllib.request
import urllib.parse
import glob
import sqlite3
import os
import sys
from http import cookiejar
import json
import time
import lxml.html


LOGIN_EMAIL = 'txtxw@163.com'
LOGIN_PASSWORD = 'a123456'
LOGIN_URL = 'http://example.webscraping.com/places/default/user/login'
DOMAIN_URL = 'example.webscraping.com'


def login_basic():
    """fails because not using formkey
    """
    data = {'email': LOGIN_EMAIL, 'password': LOGIN_PASSWORD}
    encoded_data = urllib.parse.urlencode(data).encode(encoding='utf-8')
    request = urllib.request.Request(LOGIN_URL, encoded_data)
    response = urllib.request.urlopen(request)
    print(response.geturl())


def login_formkey():
    """fails because not using cookies to match formkey
    """
    html = urllib.request.urlopen(LOGIN_URL).read()
    data = parse_form(html)
    data['email'] = LOGIN_EMAIL
    data['password'] = LOGIN_PASSWORD
    encoded_data = urllib.parse.urlencode(data).encode(encoding='utf-8')
    request = urllib.request.Request(LOGIN_URL, encoded_data)
    response = urllib.request.urlopen(request)
    print(response.geturl())


def login_cookies():
    """working login
    """
    cj = cookiejar.CookieJar()
    cookie_handler = urllib.request.HTTPCookieProcessor(cj)
    opener = urllib.request.build_opener(cookie_handler)
    html = opener.open(LOGIN_URL).read()
    data = parse_form(html)
    data['email'] = LOGIN_EMAIL
    data['password'] = LOGIN_PASSWORD
    encoded_data = urllib.parse.urlencode(data).encode(encoding='utf-8')
    request = urllib.request.Request(LOGIN_URL, encoded_data)
    response = opener.open(request)
    print(response.geturl())
    return opener

def login_cookies_file():
    """working login
    """
    filename = "cookie.txt"
    cj = cookiejar.MozillaCookieJar(filename)
    cookie_handler = urllib.request.HTTPCookieProcessor(cj)
    opener = urllib.request.build_opener(cookie_handler)
    html = opener.open(LOGIN_URL).read()
    data = parse_form(html)
    data['email'] = LOGIN_EMAIL
    data['password'] = LOGIN_PASSWORD
    encoded_data = urllib.parse.urlencode(data).encode(encoding='utf-8')
    request = urllib.request.Request(LOGIN_URL, encoded_data)
    response = opener.open(request)
    print(response.geturl())
    cj.save(ignore_discard=True, ignore_expires=True)
    return opener

def login_from_cookies_file():

    """load cookies from firefox
    """
    session_filename = find_ff_sessions()
    cj = cookiejar.MozillaCookieJar()
    cj.load('cookie.txt', ignore_discard=True, ignore_expires=True)
    cookie_handler = urllib.request.HTTPCookieProcessor(cj)
    opener = urllib.request.build_opener(cookie_handler)
    html = opener.open(LOGIN_URL).read()

    tree = lxml.html.fromstring(html)
    print(tree.cssselect('ul#navbar li a')[0].text)
    return opener


def login_firefox():
    """load cookies from firefox
    """
    session_filename = find_ff_sessions()
    cj = load_ff_sessions(session_filename)
    cookie_handler = urllib.request.HTTPCookieProcessor(cj)
    opener = urllib.request.build_opener(cookie_handler)
    html = opener.open(LOGIN_URL).read()

    tree = lxml.html.fromstring(html)
    print(tree.cssselect('ul#navbar li a')[0].text)
    return opener


def parse_form(html):
    """extract all input properties from the form
    """
    tree = lxml.html.fromstring(html)
    data = {}
    for e in tree.cssselect('form input'):
        if e.get('name'):
            data[e.get('name')] = e.get('value')
    return data



def load_ff_sessions(session_filename):
    cj = cookiejar.CookieJar()
    if os.path.exists(session_filename):
        try:
            json_data = json.loads(open(session_filename, 'rb').read())
        except ValueError as e:
            print('Error parsing session JSON:', str(e))
        else:
            for window in json_data.get('windows', []):
                for cookie in window.get('cookies', []):
                    import pprint; pprint.pprint(cookie)
                    c = cookiejar.Cookie(0, cookie.get('name', ''), cookie.get('value', ''),
                        None, False,
                        cookie.get('host', ''), cookie.get('host', '').startswith('.'), cookie.get('host', '').startswith('.'),
                        cookie.get('path', ''), False,
                        False, str(int(time.time()) + 3600 * 24 * 7), False,
                        None, None, {})
                    cj.set_cookie(c)
    else:
        print('Session filename does not exist:', session_filename)
    return cj


def find_ff_sessions():
    paths = [
        '~/.mozilla/firefox/*.default',
        '~/Library/Application Support/Firefox/Profiles/*.default',
        '%APPDATA%/Roaming/Mozilla/Firefox/Profiles/*.default'
    ]
    for path in paths:
        filename = os.path.join(path, 'sessionstore.js')
        matches = glob.glob(os.path.expanduser(filename))
        if matches:
            return matches[0]


def main():
    # login_cookies_file()
    # login_firefox()
    login_from_cookies_file()

if __name__ == '__main__':
    main()
