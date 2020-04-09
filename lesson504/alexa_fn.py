#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/2/27 0:33
# @Author  : tanxw
# @Desc    : 解析Alexa列表

import csv
from zipfile import ZipFile
from io import StringIO, BytesIO
from lesson503.downloader import Downloader
import codecs

def alexa():
    D = Downloader()
    zipped_data = D('http://s3.amazonaws.com/alexa-static/top-1m.csv.zip')
    urls = [] # top 1 million URL's will be stored in this list
    with ZipFile(BytesIO(zipped_data)) as zf:
        csv_filename = zf.namelist()[0]
        # 此处代码读取一直报错，改为比较简单的读取方式
        # for _, website in csv.reader(zf.open(csv_filename)):
        #     urls.append('http://' + website)
        get_csv_urls(zf, csv_filename, urls)
    return urls

def get_csv_urls(zf, csv_filename, urls):
    content = zf.open(csv_filename)
    while True:
        row = content.readline().decode('utf8')
        if not row:
            break
        col = row.split(',')
        url = 'http://' + col[1].replace('\n', '')
        urls.append(url)
    print(urls)


if __name__ == '__main__':
   print(len(alexa()))