#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/2/25 21:09
# @Author  : tanxw
# @Desc    : 为链接爬虫添加抓取回调

import csv
import re
import urllib.parse
import lxml.html
from lesson502.link_crawler import link_crawler

FIELDS = ('area', 'population', 'iso', 'country', 'capital', 'continent', 'tld', 'currency_code', 'currency_name', 'phone', 'postal_code_format', 'postal_code_regex', 'languages', 'neighbours')


def scrape_callback(url, html):
    if re.search('/places/', url):
        tree = lxml.html.etree.HTML(html)
        row = [tree.cssselect('table > tr#places_{}__row > td.w2p_fw'.format(field))[0].text for field in FIELDS]
        print(url, row)


if __name__ == '__main__':
    link_crawler('http://example.webscraping.com/', '/(index|view|places)', scrape_callback=scrape_callback)
