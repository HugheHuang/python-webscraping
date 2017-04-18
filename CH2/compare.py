#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
__title__ = 'scraping_source'
__author__ = 'Hughe'
__time__ = '2017-04-05  16:37'
"""

Field=('area','population','iso','country','capital','continent',
       'tld','currency_code','currency_name','phone',
       'postal_code_format','postal_code_regex','languages',
       'neighbours')

import re
def re_scrap(html):
    results={}
    for field in Field:
        results[field]=re.search('<tr id="places_%s__row">.*?<td class="w2p_fw">(.*?)</td>' % field,html).groups()[0]
    return results

from bs4 import  BeautifulSoup
def bs_scrap(html):
    soup=BeautifulSoup(html,'html.parser')
    results={}
    for field in Field:
        results[field]=soup.find('table').find('tr',id=
            'places_%s__row' % field).find('td',class_='w2p_fw').text
    return results

import lxml.html
def lxml_scrap(html):
    tree=lxml.html.fromstring(html)
    results={}
    for field in Field:
        results[field]=tree.cssselect('table>tr#places_%s__row > td.w2p_fw' % field)[0].text_content()
    return results

if __name__ == '__main__':
    import time
    from link_crawler import download
    NUM_ITERATIONS=1000
    html=download('http://example.webscraping.com'
                  '/places/view/United-Kingdom-239')
    for name,scraper in [('regular expressions',re_scrap),
                         ('beautifulsoup',bs_scrap),('lxml',lxml_scrap)]:
        start=time.time()
        for i in range(NUM_ITERATIONS):
            if scraper==re_scrap:
                re.purge()
            result=scraper(html)
            #print result
            assert(result['area']=='244,820 square kilometres')
        end=time.time()
        print '%s: %.2f seconds' % (name,end-start)


