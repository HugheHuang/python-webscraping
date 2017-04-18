#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__  = mongo_cache.py
__author__ = Hughe
__time__   = 2017-04-09 10:52
"""

from datetime import datetime,timedelta
from pymongo import MongoClient
from link_crawler import link_crawler

class MongoCache:
    def __init__(self,client=None,expires=timedelta(day=30)):
        #如果客户端不存在就在mongo里面创建一个
        self.client=MongoClient('localhost',20717) if client is None else client
        #创建连接储存缓存网页
        self.db=client.cache
        #创建文件失效索引
        self.db.webpage.create_index('timestamp',
            expireAfterSeconds=expires.total_seconds())

    def __getitem__(self, url):
        record=self.db.webpage.find_one({'_id':url})
        if record:
            return record['result']
        else:
            raise KeyError(url+' does not exist')

    def __setitem__(self, url, result):
        record={'result':result,'timestamp':datetime.utcnow()}
        self.db.webpage.update({'_id':url},{'$set':record},upsert=True)

if __name__ == '__main__':
    link_crawler('http://example.webscraping.com/', '/(index|view)', cache=MongoCache())
