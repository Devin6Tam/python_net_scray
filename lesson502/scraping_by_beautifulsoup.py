#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/2/25 12:39
# @Author  : tanxw
# @Desc    : 抓取数据-beautifulsoup

# 安装beautifulsoup4
# pip install beautifulsoup4

from bs4 import BeautifulSoup
import lesson501.link_crawler

broken_html = '<ul class=country><li>Area<li>Population</ul>'
# parse the Html
soup = BeautifulSoup(broken_html,'html.parser')
fixed_html = soup.prettify()
print(fixed_html)

"""
从上面的执行结果中可以看出，BeautifulSoup能够正确解析缺失的
引号并闭合标签，此外还添加了<html>和<body>标签使其成为完整的
HTML 文档。现在可以使用find()和find_all()方法来定位我们需要的
元素了。
"""

ul = soup.find('ul', attrs={'class':'country'})
# result just the first match
first_match = ul.find('li')
print(first_match)
# return all matches
all_matches = ul.find_all('li')
print(all_matches)

# 下面使用该方法抽取示例国家面积数据的完整代码。
url = 'http://example.webscraping.com/places/default/view/Aland-Islands-2'
headers = {'User-agent': 'MzblocCrawler'}
html = lesson501.link_crawler.download(url, headers, proxy=None, num_retries=2)
soup = BeautifulSoup(html.decode('utf8'), 'html.parser')
# locate the area row
tr = soup.find(attrs={'id':'places_area__row'})
# locate the area tag
td = tr.find(attrs={'class':'w2p_fw'})
# extract the next from this tag
area = td.text
print(area)

"""
这段代码虽然比正则表达式的代码更加复杂， 但更容易构造和理解。
而且，像多余的空格和标签属性这种布局上的小变化， 我们也无须再担心了。
"""