#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
__title__ = 'test_02'
__author__ = 'Hughe'
__time__ = '2017-04-07  23:32'
"""
import re
import lxml.html
import link_crawler
Field=('area','population','iso','country','capital','continent',
       'tld','currency_code','currency_name','phone',
       'postal_code_format','postal_code_regex','languages',
       'neighbours')

def scrape_callback(url,html):
    if re.search('/view/',url):
        tree=lxml.html.fromstring(html)
        row=[tree.cssselect('table > tr#places_%s__row > td.w2p_fw' % field)[0].text_content() for field in Field]
        print url,row

import csv
class ScrapeCallback:
    def __init__(self):
        self.writer=csv.writer(open('countries.csv','w'))
        self.fields = ('area', 'population', 'iso', 'country', 'capital', 'continent',
                 'tld', 'currency_code', 'currency_name', 'phone',
                 'postal_code_format', 'postal_code_regex', 'languages',
                 'neighbours')
        self.writer.writerow(self.fields)
    def __call__(self, url,html):
        if re.search('/view/', url):
            tree = lxml.html.fromstring(html)
            row = []
            for field in self.fields:
                row.append(tree.cssselect('table > tr#places_{}__row > td.w2p_fw'.format(field))[0].text_content())
            self.writer.writerow(row)

if __name__ == '__main__':

    link_crawler.link_crawler('http://example.webscraping.com', '/(index|view)',
                              delay=0, num_retries=1, user_agent='GoodCrawler',
                              scrape_callback=ScrapeCallback())

