#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/2/27 11:20
# @Author  : tanxw
# @Desc    : 多线程爬虫测试

import sys
from lesson504.threaded_crawler import threaded_crawler
from lesson504.threaded_crawler1 import threaded_crawler1
from lesson503.mongo_cache import MongoCache
from lesson504.alexa_cb import AlexaCallback
import multiprocessing

def main(max_threads):
    scrape_callback = AlexaCallback()
    cache = MongoCache()
    cache.clear()
    threaded_crawler(scrape_callback.seed_url, scrape_callback=scrape_callback, cache=cache, max_threads=max_threads, timeout=10)


def process_link_crawler(args, **kwargs):
    num_cpus = multiprocessing.cpu_count()
    print('Starting %d processes' % num_cpus)
    processes = []
    for i in range(num_cpus):
        p = multiprocessing.Process(target=threaded_crawler1, args=[args], kwargs=kwargs)
        p.start()
        processes.append(p)
    for p in processes:
        p.join()


if __name__ == '__main__':
    # max_threads = int(sys.argv[1])
    max_threads = 3
    main(max_threads)
