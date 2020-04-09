#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/2/24 17:21
# @Author  : tanxw
# @Desc    : 对目标网站进行背景调研

# 1. 检查robots.txt
# curl http://example.webscraping.com/robots.txt
"""
# section 1
User-agent: BadCrawler
Disallow: /

# section 2
User-agent: *
Disallow: /trap
Crawl-delay: 5

# section 3
Sitemap: http://example.webscraping.com/sitemap.xml
"""

# 2. 检查网站地图
# curl http://example.webscraping.com/sitemap.xml
# 下面仅展示部分信息来说明
"""
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
	<url>
		<loc>http://example.webscraping.com/places/default/view/Afghanistan-1</loc>
	</url>
	<url>
		<loc>http://example.webscraping.com/places/default/view/Aland-Islands-2</loc>
	</url>
...
</urlset>
"""


# 3.识别网站所用技术-检查网站构建的技术类型
# pip install builtwith
import builtwith
print(builtwith.parse("http://example.webscraping.com"))

# 4.寻找网站所有者
# pip install whois
import whois
print(whois.whois("appspot.com"))