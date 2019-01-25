#coding=utf-8

import threading
import re
import requests
import urllib2
import json

URL = []
def get_content(key):
    header = dict()
    header['Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
    header['Accept-Encoding'] = 'gzip,deflate,sdch'
    header['Accept-Language'] = 'en-US,en;q=0.8'
    header['Connection'] = 'keep-alive'
    header['DNT'] = '1'
    header['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; WOW64)'
    root = 'https://s.taobao.com/search?q='
    params = '&imgfile=&commend=all&ssid=s5-e&search_type=item&sourceId=tb.index&spm=a21bo.2017.201856-taobao-item.1&ie=utf8&initiative_id=tbindexz_20170306'

    url = root + key + params
    URL.append(url)
    req = requests.get(url, headers = header,timeout=3)
    return req.content

def reg_Findall(spider_content):
    '''根据抓取经验 json有两种不同的key 采用两种不同的正则去匹配相应的key-value'''
    goods = []
    price = re.findall(r'"view_price":"([^"]+)"', spider_content, re.I)
    title = re.findall(r'"raw_title":"([^"]+)"', spider_content, re.I)
    sales = re.findall(r'"view_sales":"([^"]+)"', spider_content, re.I)
    pic_url = re.findall(r'"pic_url":"([^"]+)"', spider_content, re.I)
    baobei = re.findall(r'"url":"([^"]+)"', spider_content, re.I)
    if len(price) != 0 and len(title) != 0 and len(title) != 0:
        pic_src = []  # real url of pic
        baibei_url = []  # real url of baobei
        # two for loop to find real pic_src and baobei_url
        i = 1
        while i < len(baobei)-2:
            baobei_url.append(baobei[i].decode('unicode-escape').encode('utf8'))
            i = i + 2;

        for i in range(len(title)):
            pic_src.append(pic_url[i])
        goods.append(title)
        goods.append(price)
        goods.append(sales)
        goods.append(pic_src)
        goods.append(baobei_url)
    else:
        # pattern 1未成功 则采用pattern 2去匹配
        title_2 = re.findall(r'"title":"([^"]+)"', spider_content, re.I)
        price_2 = re.findall(r'"price":"([^"]+)"', spider_content, re.I)
        sales_2 = re.findall(r'"month_sales":"([^"]+)"', spider_content, re.I)
        pic_url = re.findall(r'"pic_url":"([^"]+)"', spider_content, re.I)
        baobei = re.findall(r'"url":"([^"]+)"', spider_content, re.I)

        baobei_url = []
        pic_src = []

        if len(title_2) != 0 and len(price_2) != 0 and len(sales_2) != 0:
            i = 1
            while i < len(baobei) - 2:
                baobei_url.append(baobei[i].decode('unicode-escape').encode('utf8'))
                i = i + 2;
            for i in range(len(title_2)):
                pic_src.append(pic_url[i])
            goods.append(title_2)
            goods.append(price_2)
            goods.append(sales_2)
            goods.append(pic_src)
            goods.append(baobei_url)
    return goods


def start_spider(key):
    '''The type of the data spidered from taobao is Json!'''
    content = get_content(key)
    json_content = re.findall(r'g_page_config = (.*);', content)

    # title price sales
    good_dic = []
    if len(json_content) != 0:
        good_dic = reg_Findall(content)
    else:
        while len(json_content) == 0:
            # 尽量规避淘宝反爬虫 若获取的json数据为空 则两秒后重复抓取 直到获取数据
            threading._sleep(2)

            content = get_content(key)
            json_content = re.findall(r'g_page_config = (.*);', content)
            good_dic = reg_Findall(content)
    return good_dic


def get_URL():
    return URL
