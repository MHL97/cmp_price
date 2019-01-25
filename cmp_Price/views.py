# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.shortcuts import render
from django.http import HttpResponse

# import spider
from spider import JingDong as spiderJD
from spider import Taobao as spiderTB
def home(request):
    return render(request, 'cmp_Price/base.html')

def search(request):
    postKey = request.POST['key']

    goodsJD = spiderJD.start_spider(postKey)
    goodsTB_temp = spiderTB.start_spider(postKey)

    TB_URL = spiderTB.get_URL()
    JD_URL = spiderJD.get_URL()
    tb_URL = TB_URL[0]
    jd_URL = JD_URL[0]
    goodsTB = []
    titles = goodsTB_temp[0]
    prices = goodsTB_temp[1]
    sales = goodsTB_temp[2]
    pic = goodsTB_temp[3]
    baobei = goodsTB_temp[4]
    for i in range(len(titles)):
        dic_temp = {}
        dic_temp['title'] = titles[i]
        dic_temp['price'] = prices[i]
        dic_temp['sales'] = sales[i]
        dic_temp['pic_url'] = pic[i]
        dic_temp['baobei_url'] = baobei[i]
        goodsTB.append(dic_temp)

    return render(request, 'cmp_Price/searchResult.html',{
        'goodsJD':goodsJD,
        'goodsTB':goodsTB,
        'tb_URL':tb_URL,
        'jd_URL':jd_URL
    })
