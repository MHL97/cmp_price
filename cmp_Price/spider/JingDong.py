# -*- coding: utf-8 -*-
import urllib2
import re
import requests
from HTMLParser import HTMLParser

URL = []
def _attr(attrs, attrname):
    for attr in attrs:
        if attrname == attr[0]:
            return attr[1]
    return None

class get_goods(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.price = []
        self.title = []
        self.src = []
        self.commit = []
        self.pic_src = []
        self.in_li = False
        self.find_price = False
        self.in_img = False
        self.find_src = False
        self.in_i = False
        self.in_commit = False
    def handle_starttag(self, tag, attrs):
        if tag == 'li' and _attr(attrs, 'class') == 'gl-item':
            self.in_li = True
        if tag == 'div' and _attr(attrs, 'class') == 'p-price':
            self.find_price = True
        if tag == 'i' and self.find_price:
            self.in_i =True
        if self.in_li and tag == 'div' and _attr(attrs, 'class') == 'p-img':
            self.in_img = True
        if self.in_img and tag == 'a':
            title = _attr(attrs, 'title')
            self.src.append(_attr(attrs, 'href'))
            self.title.append(title)
            self.find_src = True
        if self.find_src and tag == 'img':
            if _attr(attrs, 'data-lazy-img') != None:
                self.pic_src.append(_attr(attrs, 'data-lazy-img'))
            else:
                self.pic_src.append(_attr(attrs, 'src'))
        if tag == 'div' and _attr(attrs, 'class') == 'p-commit':
            self.in_commit = True
    def handle_endtag(self, tag):
        if tag == 'li':
            self.in_li = False
        if tag == 'div':
            self.in_img = False
            self.find_price = False
            self.in_commit = False
        if tag == 'a':
            self.find_src = False
        if tag == 'i':
            self.in_i = False
    def handle_data(self, data):
        if self.in_i:
            self.price.append(data)
        if self.in_commit:
            commits = re.findall(r'.*[+]', data)
            for item in commits:
                if item != None:
                    self.commit.append(item)
def find_min(a, b, c, d):
    min = a
    if b < min:
        min = b
    if c < min:
        min = c
    if d < min:
        min = d
    return min

def start_spider(key):
    '''start spider JD and return result dict'''
    result = []
    root = 'https://search.jd.com/Search?keyword='
    params = '&enc=utf-8'
    url = root + key + params
    URL.append(url)
    req = requests.get(url)
    parser = get_goods()

    parser.feed(req.text.encode('ISO-8859-1').decode('utf8'))
    titles = parser.title
    hrefs = parser.src
    prices = parser.price
    commits = parser.commit
    pic_URL = parser.pic_src
    min_range = find_min(len(titles), len(hrefs), len(prices), len(commits))

    for i in range(min_range):
        temp_dic = {}
        temp_dic['title'] = titles[i]
        temp_dic['src'] = hrefs[i]
        temp_dic['price'] = prices[i]
        temp_dic['commit'] = commits[i]
        temp_dic['pic_url'] = pic_URL[i]
        result.append(temp_dic)

    return result
def get_URL():
    '''get URL dict'''
    return URL