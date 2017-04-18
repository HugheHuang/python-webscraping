#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__  = threaded_test.py
__author__ = Hughe
__time__   = 2017-04-09 15:53
"""

import sys
from threaded_crawler import threaded_crawler
from mongo_cache import MongoCache
from alexa_cb import AlexaCallback
from disk_cache import DiskCache
from link_crawler import  link_crawler
def main(max_threads):

    cache = MongoCache()
    # cache.clear()
    threaded_crawler(seed_url='http://example.webscraping.com',scrape_callback= link_crawler('http://example.webscraping.com'), cache=cache, max_threads=max_threads,
                     timeout=0)


if __name__ == '__main__':
    main(5)
