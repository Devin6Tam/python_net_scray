#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/2/25 13:23
# @Author  : tanxw
# @Desc    : 抓取数据-lxml

"""
Lxml是基于libxml2这一XML解析库的Python封装。该模块使用C
语言编写， 解析速度比Beautiful Soup更快，不过安装过程也更为复杂。最新
的安装说明可以参考http://Lxml.de/installation.html
"""
# 安装命令
# pip install lxml
# pip install cssselect

import lxml.html
import cssselect
import lesson501.link_crawler


broken_html = '<ul class=country><li>Are<li>Population></ul>'
# parse the html
tree = lxml.html.fromstring(broken_html)
fixed_html = lxml.html.tostring(tree, pretty_print=True)
print(fixed_html)

# lxml也可以正确解析属性两侧缺失的引号，并闭合标签，不过
# 该模块没有额外添加<html>和<body>标签。

# 选择元素的步骤，有几种不同方法
# XPath选择器类似BeautifulSoup的find()方法
# CSS选择器，比较简洁，可以动态解析内容，并复用起来
# jQuery 选择器，基于javascript,需要有一定的基础


url = 'http://example.webscraping.com/places/default/view/Aland-Islands-2'
headers = {'User-agent': 'MzblocCrawler'}
html = lesson501.link_crawler.download(url, headers, proxy=None, num_retries=2)
tree = lxml.html.etree.HTML(html)
td = tree.cssselect('tr#places_area__row > td.w2p_fw')[0]
area = td.text
print(area)

"""
css 选择器
css 选择器表示选择元素所使用的模式。下面是一些常用的选择器示例。
需要注意的是，lxml在内部实现中，实际上是将css选择器转换为等价的XPath 选择器。

选择所有标签：＊
选择<a>标签：a
选择所有class="link"的元素: .link
选择class="link"的<a>标签：a.link
选择id="home"的<a>标签：aJf home
选择父元素为<a>标签的所有<span>子标签：a > span
选择<a>标签内部的所有<span>标签：a span
选择title属性为"Home"的所有<a>标签：a [title=Home]

支持大部分的CSS属性，不支持的功能参考：https://cssselect.readthedocs.io/en/latest/
W3C己提出CSS3规范，其网址为:https://www.w3.org/TR/2018/REC-selectors-3-20181106/
"""