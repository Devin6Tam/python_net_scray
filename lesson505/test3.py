#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/2/28 13:49
# @Author  : tanxw
# @Desc    : selenium 动态渲染页面

# 官方说明文档
# https://python-selenium-zh.readthedocs.io/zh_CN/latest

# pip install selenium
# chromedriver 插件下载
# 点击Google菜单帮助 -> 关于GoogleChrome -> 查看版本号（69.0.3497.100（正式版本）（32 位）
# https://sites.google.com/a/chromium.org/chromedriver/downloads  查看对应版本号 2.41~2.44
# https://chromedriver.storage.googleapis.com/index.html 选择对应版本号的插件压缩包
# 解压位置
# 本地存放脚本目录： D:\python\Envs\system_env\Scripts [本人设置的system_evn虚拟环境]
# chromedriver验证
# 验证： cmd命令行 执行 chromedriver 输出如下信息：
# Starting ChromeDriver 2.42.591088 (XXX) on port 9515
# Only local connections are allowed.
# geckodriver 插件下载
# https://github.com/mozilla/geckodriver/releases  最新版本v0.26.0 支持firefox>=60.0
# 在firefox--> web开发者--> 获取更多工具--> 选择Selenium IDE--> add to firefox  [未设置也能满足使用]
# 解压位置
# 本地存放脚本目录： D:\python\Envs\system_env\Scripts [本人设置的system_evn虚拟环境]

from selenium import webdriver
import os
"""
示例：后台执行
from selenium.webdriver.firefox.options import Options
options = Options()
options.add_argument('-headless')
driver = webdriver.Firefox(options=options)  
"""
# driver = webdriver.Firefox()  # firefox浏览器
driver = webdriver.Chrome()    # Chrome浏览器
# driver.get('https://www.jianshu.com')  # 打开简书
driver.get('http://example.webscraping.com/places/default/search')
driver.find_element_by_id('search_term').send_keys('.')
driver.execute_script("document.getElementById('page_size').options[1].text = '1000'");
driver.find_element_by_id('search').click()
# 超时时间
# driver.implicitly_wait(3)
driver.implicitly_wait(30)
links = driver.find_elements_by_css_selector('#results a')
countries = [link.text for link in links]
driver.close()
print(countries)
# 加入这条代码，解决chromedriver进程无法关闭问题
os.system("taskkill /f /im chromedriver.exe")
# os.system('taskkill /im chromedriver.exe /F')