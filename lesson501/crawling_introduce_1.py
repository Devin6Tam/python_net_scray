#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/2/24 18:02
# @Author  : tanxw
# @Desc    : 实现一个简单的爬虫
"""
    python3版本中,urllib,urllib2已合并，统一使用urllib模块
"""
import urllib.request
import urllib.error
import re
import itertools
import urllib.parse
import urllib.robotparser


delay = 10
# 下载网页
def download(url, user_agent='wswp', proxy=None, num_retries=3):
	print('Downloading: %s' % url)
	headers = {'User-agent': user_agent}
	request = urllib.request.Request(url, headers=headers)

	opener = urllib.request.build_opener()
	if proxy:
		proxy_params = {urllib.parse.urlparse(url).scheme: proxy}
		opener.add_handler(urllib.request.ProxyHandler(proxy_params))
	try:
	    # html = urllib.request.urlopen(request).read()
		html = opener.open(request).read()
	except urllib.error.URLError as e:
		print('Download error:', e.reason)
		html = None
		if num_retries > 0:
			if hasattr(e, 'code') and 500 <= e.code < 600:
				throttle = Throttle(delay)
				throttle.wait(url)
				return download(url, user_agent, proxy, num_retries-1)
	return html

# 网站地图爬虫
def crawl_sitemap(url):
	# 下载网站地图文件
	sitemap = download(url)
	# 提取网站地图链接
	links = re.findall(r'<loc>(.*?)</loc>', sitemap.decode('utf8'))
	# 遍历获取每个站点链接，并且下载
	for link in links:
		html = download(link)
		print(html)

# ID遍历爬虫
def crawling_by_id():
	# maximum number of consecutive download errors allowed
	max_errors = 5
	# current number of consecutive download errors
	num_errors = 0
	for page in itertools.count(1):
		url = 'http://example.webscraping.com/view/-%d' % page
		html = download(url)
		if html is None:
			# 抓取网页数据失败（ID 不连续）
			num_errors += 1
			if num_errors == max_errors:
				break
		else:
			# 成功抓取了网页
			num_errors = 0

def link_crawler(seed_url, link_regex, user_agent='wswp', max_depth = 2):
	# 爬取链接地址列表
	crawl_queue = [seed_url]
	# 记录已爬取链接地址集合
	# seen = set(crawl_queue)
	seen2 = {seed_url: 0}
	max_depth = 2

	rp = urllib.robotparser.RobotFileParser()
	rp.set_url('http://example.webscraping.com/robots.txt')
	rp.read()

	# 循环爬取来源地址 crawl_queue
	while crawl_queue:
		# 获取末尾项，并删减
		url = crawl_queue.pop()
		depth = seen2[url]
		if depth != max_depth:
			if rp.can_fetch(user_agent, url):
				html = download(url)

				# 使用正则表达式筛选出想要的链接地址 get_links(html)
				for link in get_links(html):
					# 匹配相应的链接地址
					if re.match(link_regex, link):
						# 将相对的链接地址转换为绝对链接，以便定位网页
						link = urllib.parse.urljoin(seed_url, link)
						if link not in seen2:
							# 收藏记录已被爬过的链接地址，下次爬取之前主动过滤
							# seen.add(link)
							seen2[link] = depth + 1
							crawl_queue.append(link)
			else:
				print("Blocked by robots.txt: %s" % url)


def get_links(html):
	webpage_regex = re.compile('<a[^>]+href=["\'](.*?)["\']', re.IGNORECASE)
	return webpage_regex.findall(html.decode("utf8"))

import datetime
import time
# 下载限速
class Throttle:
	def __init__(self, delay):
		self.delay = delay
		self.domains = {}

	def wait(self, url):
		domain = urllib.parse.urlparse(url).netloc
		last_accessed = self.domains.get(domain)

		if self.delay > 0 and last_accessed is not None:
			sleep_secs = self.delay - (datetime.datetime.now() - last_accessed).seconds
			if sleep_secs > 0:
				time.sleep(sleep_secs)
		self.domains[domain] = datetime.datetime.now()


# 高级功能
# 解析robots.txt文件，以避免下载禁止爬取的URL。
# import urllib.robotparser
# rp = urllib.robotparser.RobotFileParser()
# rp.set_url('http://example.webscraping.com/robots.txt')
# rp.read()
# url = 'http://example.webscraping.com'
# user_agent = 'BadCrawler'
# print(rp.can_fetch(user_agent, url))
# user_agent = 'GoogleCrawler'
# print(rp.can_fetch(user_agent, url))


# 支持代理
# proxy = None
# opener = urllib.request.build_opener()
# url = 'http://example.webscraping.com'
# proxy_params = {urllib.parse.urlparse(url).scheme: proxy}
# opener.add_handler(urllib.request.ProxyHandler(proxy_params))
# headers = {'User-agent': "wswp"}
# request = urllib.request.Request(url, headers=headers)
# response = opener.open(request)

seed_url = 'http://example.webscraping.com/places'
link_regex = '/(index|view|places)'
link_crawler(seed_url, link_regex, user_agent='MzblocCrawler')


# link_crawler('http://example.webscraping.com', '/(index|view|places)')
# crawling_by_id()
# crawl_sitemap('http://example.webscraping.com/sitemap.xml')
# default_user_agent = "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36"
# print(download("http://example.webscraping.com", 3))
