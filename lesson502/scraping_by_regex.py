#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/2/25 12:14
# @Author  : tanxw
# @Desc    : 数据抓取-正则表达式

import re
import lesson501.link_crawler

url = 'http://example.webscraping.com/places/default/view/Afghanistan-1'
headers = {'User-agent': 'MzblocCrawler'}
html = lesson501.link_crawler.download(url, headers, proxy=None, num_retries=2)
if html:

    # 网页发生变化，该方案可能就会失效。
    # 如果还希望未来还可以继续抓取该数据，我们给出更健壮的方案，把其父元素<tr> 也加入进来，有id属性，是唯一的
    # content = re.findall('<td class="w2p_fw">(.*?)</td>', html.decode("utf8"))[1]

    content = re.findall('<tr id="places_area__row"><td class="w2p_fl"><label class="readonly" for="places_area" id="places_area__label">Area: </label></td><td class="w2p_fw">(.*?)</td>', html.decode("utf8"))
    print(content)

"""
虽然该正则表达式更容易适应未来变化， 但又存在难以构造、可读性差的问题。
此外， 还有一些微小的布局变化也会使该正则表达式无法满足， 比如在＜ td＞标签里添加t i t l e 属性。
从本例中可以看出， 正则表达式为我们提供了抓取数据的快捷方式， 但是该方法过于脆弱， 容易在网页更新后出现问题。
幸好， 还有一些更好的解决方案， 我们会在接下来继续介绍。
"""