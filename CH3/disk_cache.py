#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__  = disk_cache.py
__author__ = Hughe
__time__   = 2017-04-08 17:19
"""

import os
import re
import urlparse
import pickle
from link_crawler import  link_crawler
import zlib
from datetime import datetime,timedelta
class DiskCache:
    #加入默认30天周期的清理过期检查 expires
    def __init__(self,cache_dir='cache',expires=timedelta(seconds=5)):
        self.cache_dir=cache_dir
        self.expires=expires
        #self.max_length=max_length

    #应用了文件名限制
    def url_to_path(self,url):
        #解析url
        components=urlparse.urlsplit(url)
        path=components.path
        if not path:
            path='index.html'
        elif path.endswith('/'):
            path+='index.html'
        filename=components.netloc+path+components.query
        filename=re.sub('[^/0-9a-zA-Z\-.,;_]','_',filename)
        filename='/'.join(segment[:255] for segment in filename.split('/'))
        return os.path.join(self.cache_dir,filename)

    #get cache[url]
    def __getitem__(self,url):
        path=self.url_to_path(url)
        if os.path.exists(path):
            with open(path,'rb') as fp:
                result,timestamp= pickle.loads(zlib.decompress(fp.read()))
                if self.has_expires(timestamp):
                    raise KeyError(url+'has expired')
                return result

                """ 加入时间戳之前版本：
                #加入解压   原版本：return pickle.load(fp)
                return pickle.loads(zlib.decompress(fp.read()))"""
        else:
            raise KeyError(url+'does not exist')

    #set result=cache[url]
    def __setitem__(self, url, result):
        path=self.url_to_path(url)
        folder=os.path.dirname(path)
        timestamp=datetime.utcnow()
        data=pickle.dumps((result,timestamp))
        if not os.path.exists(folder):
            os.makedirs(folder)
        with open(path,'wb') as fp:
            #加入压缩 原版本：fp.write(pickle.dumps(result))
            fp.write(zlib.compress(data))

    #检查是否过期
    def has_expires(self,timestamp):
        return datetime.utcnow()>timestamp+self.expires
if __name__ == '__main__':
    link_crawler('http://example.webscraping.com/', '/(index|view)', cache=DiskCache())



