#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/3/3 0:27
# @Author  : tanxw

# pip install scrapely
from scrapely import Scraper
s = Scraper()
train_url = 'http://example.webscraping.com/places/default/view/Afghanistan-1'
s.train(train_url, {'name': 'Afghanistan', 'population': '29,121,286'})
test_url = 'http://example.webscraping.com/places/default/view/United-Kingdom-239'
s.scrape(test_url)
