#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# @Time    : 2017/4/4 0004 15:20
# @Author  : Hughe
# @File    : test_01.py
import re
from link_crawler import download
"""
正则表达式法---------------------------------------------------------------
"""
def test_re():
    url='http://example.webscraping.com/view/United-Kingdom-239'
    html=download(url)
    print re.findall('<tr id="places_area__row">.*?<td\s*class=["\']w2p_fw["\']>(.*?)</td>',html)[0]
"""
BeautifulSoup法----------------------------------------------------------
"""
from bs4 import BeautifulSoup
def test_beautifulsoup():
    url = 'http://example.webscraping.com/view/United-Kingdom-239'
    html=download(url)
    #以下四行要理解
    soup=BeautifulSoup(html,'html.parser')
    tr=soup.find(attrs={'id':'places_area__row'})   #大致推断出find格式 attrs={'属性'：'值'}
    td=tr.find(attrs={'class':'w2p_fw'})
    area=td.text
    print area

"""
Lxml法-------------------------------------------------------------
"""
import lxml.html
def test_lxml():
    url = 'http://example.webscraping.com/view/United-Kingdom-239'
    html = download(url)
    tree=lxml.html.fromstring(html)
    td=tree.cssselect('tr#places_area__row > td.w2p_fw')[0]
    area=td.text
    print area

if __name__ == '__main__':
    test_re()
    print '~~~~~~~~~~~~~~~~~~~~~~~~~~~'
    test_beautifulsoup()
    print '~~~~~~~~~~~~~~~~~~~~~~~~~~~'
    test_lxml()


