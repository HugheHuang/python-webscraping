#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__  = search1.py
__author__ = Hughe
__time__   = 2017-04-10 09:10
"""
import json
import string
import downloader
import mongo_cache

def main():
    template_url='http://example.webscraping.com/ajax/search.json?page={}&page_size=10&seach_term={}'
    countries=set()
    download = downloader.Downloader(mongo_cache.MongoCache())

    for letter in string.lowercase:
        page=0
        while True:
            html =download(template_url.format(page, letter))
            try:
                ajax=json.loads(html)
            except ValueError as e:
                print e
                ajax = None
            else:
                for record in ajax['records']:
                    countries.add(record['country'])
            page+=1
            if ajax is None or page >=ajax ['num_pages']:
                break
    open('countries.txt','w').write('\n'.join(sorted(countries)))

try:
    from PyQt4


if __name__ == '__main__':
    main()