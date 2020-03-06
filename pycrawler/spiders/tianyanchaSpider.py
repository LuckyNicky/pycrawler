# -*- coding: utf-8 -*-
import json
import re

from scrapy import Selector
from scrapy.spiders import Spider

from ..items import *
from ..settings import *

""" 天眼查搜索API """
SEARCH_API = 'https://api9.tianyancha.com/services/v3/search/sNorV3'
""" 企业详情API """
DETAIL_API = 'https://api9.tianyancha.com/services/v3/t/common/baseinfoV5'
""" 天眼查头信息 """
REQUEST_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36",
    "version": "TYC-XCX-WX",
    "Host": "api3.tianyancha.com",
    "Authorization": '0###oo34J0WVDdeu_k1O-sWPxFpg9WJ4###1555940540033###028a568b0150721d810d5f4417e03650',
    'x-auth-token': "eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiIxODg3NTg5MjA3NSIsImlhdCI6MTU1NTk0MDU3MiwiZXhwIjoxNTU4NTMyNTcyfQ.lCJNDWQK0gD3fp9ieIlnMEzwmi00zkBqyHShdvHnspFzZQmgPHhHJAUY7mVbKY_AFk2Xhk82jMP99Q6a0wlmEQ",
}
KEYS = [
    '西湖龙井',
]

class TianYaChaSpider(Spider):
    name = 'tianyancha'
    allowed_domains = ['api.bilibili.com',
                       'bilibili.com']

    searchParams = []
    baseUrl = SEARCH_API + '/{keyword}?pageNum={pageNum}&pageSize={pageSize}&sortType={sortType}'

    start_urls = [baseUrl.format(keyword='', pageNum=1, pageSize=20, sortType=0)]

    def __init__(self, core):
        from ..utils.logger import getLogger
        self.log = getLogger()
        self.core = core


    def start_requests(self):
        for key in KEYS:
            yield scrapy.Request(
                url=self.baseUrl.format(keyword=key, pageNum=1, pageSize=20, sortType=0),
                headers=REQUEST_HEADERS,callback=self.searchParse)

    def searchParse(self, response):
        html = json.loads(response.body)

        if (html['state'] == 'ok'):
            node_list = html["data"]['companyList']
            for node in node_list:
                item = TianYanChaCompanyItem()
                item.update(company=node)
                yield scrapy.Request(url=DETAIL_API+'/{}'.format(node['id']),
                                     headers=REQUEST_HEADERS,
                                     meta={'item':item}, callback=self.DetailParse)


    def DetailParse(self, response):
        # 接收传递的item
        item = response.meta['item']

        html = json.loads(response.body)
        if (html['state'] == 'ok'):
            node = html["data"]
            item.update_detail(node)

        yield item
