#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/2/25 20:35
# @Author  : tanxw
# @Desc    : beautiful soup 抓取示例

import urllib.request
from bs4 import BeautifulSoup
import lesson502.common_download

def scrape(html):
    soup = BeautifulSoup(html.decode('utf8'), 'html.parser')
    tr = soup.find(attrs={'id':'places_area__row'}) # locate the area row
    # 'class' is a special python attribute so instead 'class_' is used
    td = tr.find(attrs={'class':'w2p_fw'})  # locate the area tag
    area = td.text  # extract the area contents from this tag
    return area

if __name__ == '__main__':
    html = lesson502.common_download.download('http://example.webscraping.com/places/default/view/Aland-Islands-2')
    print(scrape(html))