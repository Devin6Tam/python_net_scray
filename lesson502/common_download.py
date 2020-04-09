#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/2/25 20:31
# @Author  : tanxw
# @Desc    : 公用下载网页
import urllib.request
import urllib.error

def download(url, user_agent=None):
    print('Downloading:', url)
    headers = {'User-agent': user_agent or 'wswp'}
    request = urllib.request.Request(url, headers=headers)
    try:
        html = urllib.request.urlopen(request).read()
    except urllib.error.URLError as e:
        print('Download error:', e.reason)
        html = None
    return html


if __name__ == '__main__':
    print(download('http://example.webscraping.com'))
