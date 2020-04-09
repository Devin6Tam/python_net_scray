#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/2/25 20:58
# @Author  : tanxw
# @Desc    : lxml 抓取数据示例

import lxml.html
import lesson502.common_download

def scrape(html):
    tree = lxml.html.fromstring(html)
    td = tree.cssselect('tr#places_area__row > td.w2p_fw')[0]
    area = td.text
    return area

if __name__ == '__main__':
    html = lesson502.common_download.download('http://example.webscraping.com/places/default/view/Aland-Islands-2')
    print(scrape(html))
