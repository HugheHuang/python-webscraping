#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
__title__ = 'Download'
__author__ = 'Hughe'
__time__ = '2017/4/3'
"""
import urllib2
"""
带有用户代理的具有对5XX进行重试下载的下载网页函数----------------------
"""
def download( url, user_agent = 'wswp',proxy=None, num_retries =2):
    print 'Downloading:', url
    #修改用户代理名
    headers={'User_agent' : user_agent}
    request=urllib2.Request(url,headers=headers)
    #加入用户代理
    opener=urllib2.build_opener()
    if proxy:
        proxy_params={urlparse.urlparse(url).scheme:proxy}
        opener.add_handler(urllib2.ProxyHandler(proxy_params))

    try:
        html =urllib2.urlopen(request).read()
    except urllib2.URLError as e:
        print 'Download error:',e.reason
        html=None
        if num_retries > 0:
            #限制数目的重试下载
            if hasattr(e, 'code') and 500<=e.code<600:
                return download(url,user_agent,num_retries-1)
    return html

"""
网络地图爬虫--------------------------------------------------------
"""
import re
def crawl_sitemap(url):
    sitemap=download(url)
    links=re.findall('<loc>(.*?)</loc>',sitemap)
    for link in links:
        html=download(link)


"""
ID遍历爬虫---------------------------------------------------------
"""
import itertools
def ID_crawler():
    max_errors=5
    num_errors=0
    # itertools.count(1)创建了一个无限迭代器
    for page in itertools.count(1):
        url='http://example.webscraping.com/view/-%d' % page
        html=download(url)
        if html is None:
            num_errors+=1
            if num_errors==max_errors:
                break
        else:
            num_errors=0

"""
链接爬虫-----------------------------------------------------------
使用的是广度优先搜索
"""
#导入该包是为了获取绝对路径，否则只有相对路径导致urllib2报错，同时代理也会用到
import urlparse
#导入该包是为了解析robots.txt
import robotparser
def link_crawler(seed_url,link_regex):
    crawl_queue=[seed_url]
    """
    #此为先前版本，为了防止爬虫陷阱，把sean修改为字典
    #为了防止死循环（页面间的互相链接）加入seen表示已接受的链接
    #set表示生成集合，不重复
    #seen=set(crawl_queue)
    """
    #max_depth设置为负数就可以取消“避免爬虫陷阱”的功能
    #该功能维护一个字典<url,深度> 当深度超过最大深度时停止深挖
    max_depth=1
    seen={}
    #按robots.txt要求抓取  下面三行都要加入，不能少任何一行
    rp=robotparser.RobotFileParser()
    rp.set_url('http://example.webscraping.com/robots.txt')
    rp.read()
    while crawl_queue:
        url=crawl_queue.pop()
        #BadCrawler会被阻塞
        if rp.can_fetch('Crawler',url):
            #加入限速
            throttle=Throttle(delay=2000)
            throttle.wait(url)
            html=download(url)
            depth=0
            if depth !=max_depth:
                for link in get_links(html):
                    if re.match(link_regex,link):
                        #该处用到了导入包所包含的方法，使相对路径变绝对路径
                        link=urlparse.urljoin(seed_url,link)
                        if link not in seen:
                            seen[link]=depth+1
                            crawl_queue.append(link)
        else:
            print 'Block by robots.txt',url

def get_links(html):
    webpage_regex=re.compile('<a[^>]+href=["\'](.*?)["\']',re.IGNORECASE)
    return webpage_regex.findall(html)


"""
下载限速----------------------------------------------------------------------
"""
import datetime
import time
class Throttle:
    def __init__(self,delay):
        self.delay=delay
        self.domains={}

    def wait(self,url):
        domain=urlparse.urlparse(url).netloc
        last_accessed=self.domains.get(domain)
        if self.delay>0 and last_accessed is not None:
            sleep_secs=self.delay-(datetime.datetime.now()-last_accessed).seconds
            if sleep_secs>0:
                time.sleep(sleep_secs)
        self.domains[domain]=datetime.datetime.now()

if __name__=='__main__':
    # crawl_sitemap("http://example.webscraping.com/sitemap.xml")
    #ID_crawler()
    link_crawler('http://example.webscraping.com','/(index|view)')