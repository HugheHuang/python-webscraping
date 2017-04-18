#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__  = alexa_cb.py
__author__ = Hughe
__time__   = 2017-04-09 16:56
"""

import csv
from zipfile import ZipFile
from StringIO import StringIO
from mongo_cache import MongoCache


class AlexaCallback:
    def __init__(self, max_urls=1000):
        self.max_urls = max_urls
        self.seed_url = 'http://s3.amazonaws.com/alexa-static/top-1m.csv.zip'

    def __call__(self, url, html):
            if url == self.seed_url:
                urls = []
            with ZipFile(StringIO(html)) as zf:
                csv_filename = zf.namelist()[0]
                for _, website in csv.reader(zf.open(csv_filename)):
                    urls.append('http://' + website)
                    if len(urls) == self.max_urls:
                        break
            print '%%%%%%%%%'
            return urls


if __name__ == '__main__':
   print  AlexaCallback()