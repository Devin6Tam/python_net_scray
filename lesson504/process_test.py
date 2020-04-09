#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/2/27 9:56
# @Author  : tanxw
# @Desc    : 进程测试

import sys
from lesson504.process_crawler import process_crawler
from lesson503.mongo_cache import MongoCache
from lesson504.alexa_cb import AlexaCallback


def main(max_threads):
    scrape_callback = AlexaCallback()
    cache = MongoCache()
    cache.clear()
    process_crawler(scrape_callback.seed_url, scrape_callback=scrape_callback, cache=cache, max_threads=max_threads, timeout=10)


if __name__ == '__main__':
    max_threads = len(sys.argv)
    main(max_threads)
