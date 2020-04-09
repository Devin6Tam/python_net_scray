#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/2/27 0:50
# @Author  : tanxw

import csv
from zipfile import ZipFile
from io import StringIO, BytesIO
from lesson503.mongo_cache import MongoCache
from lesson503.link_crawler import link_crawler

class AlexaCallback:
    def __init__(self, max_urls=1000):
        self.max_urls = max_urls
        self.seed_url = 'http://s3.amazonaws.com/alexa-static/top-1m.csv.zip'

    def __call__(self, url, html):
        if url == self.seed_url:
            urls = []
            cache = MongoCache()
            with ZipFile(BytesIO(html)) as zf:
                csv_filename = zf.namelist()[0]
                # for _, website in csv.reader(zf.open(csv_filename)):
                #     if 'http://' + website not in cache:
                #         urls.append('http://' + website)
                #         if len(urls) == self.max_urls:
                #             break
                get_csv_urls(self, zf, csv_filename, cache, urls)
            print(urls)
            return urls

#　获取csv报表中的网站信息
def get_csv_urls(self, zf, csv_filename, cache, urls):
    content = zf.open(csv_filename)
    while True:
        row = content.readline().decode('utf8')
        if not row:
            break
        col = row.split(',')
        url = 'http://' + col[1].replace('\n', '')
        if url not in cache:
            urls.append(url)
            if len(urls) == self.max_urls:
                break

if __name__ == '__main__':
    scrape_callback = AlexaCallback()
    link_crawler(seed_url=scrape_callback.seed_url,cache = MongoCache(),
        scrape_callback = scrape_callback,ignore_robots=True)