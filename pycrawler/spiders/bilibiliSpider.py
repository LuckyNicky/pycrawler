# -*- coding: utf-8 -*-
import json, re
from scrapy.spiders import CrawlSpider, Rule, Spider
from scrapy import Selector
from ..settings import *
from ..items import *


'''
keyword: B站搜索的关键字
maxPage: 下载搜索结果前多少页
'''
RUN_PARAMS = [
    {'keyword': '猫', 'maxPage': 1},
]

SEARCH_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.167 Safari/537.36',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8'
}

DOWNLOAD_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.167 Safari/537.36',
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Referer': 'https://search.pycrawler.com/all?keyword={keyword}'
}


class BilibiliVideoSpider(Spider):
    name = 'bilibili'
    allowed_domains = ['api.bilibili.com',
                       'bilibili.com']

    runParams = RUN_PARAMS
    searchParams = []
    baseUrl = 'https://api.bilibili.com/x/web-interface/search/type?jsonp=jsonp&search_type=video&keyword={keyword}&page={maxpage}'

    start_urls = [baseUrl.format(keyword='', maxpage=1), 'http://www.bilibili.com/video/av89171088']

    def __init__(self, core):
        from ..utils.logger import getLogger
        self.log = getLogger()
        self.core = core

        if len(self.runParams) == 0:
            self.crawler.engine.close_spider(
                self,'run param should not be empty, please check the definition of RUN_PARAMS in seeting.py')
        # 校验查询条件
        for param in self.runParams:
            if param.__contains__('keyword') and param.__contains__('maxPage'):
                self.searchParams.append(param)
            else:
                self.log.debug('incalid param, ''keyword is {kv}, maxPage is {mv}'.
                                format(kv = str(param.__contains__('keyword')),
                                    mv = str(param.__contains__('maxPage'))))
        if len(self.searchParams) == 0:
            self.crawler.engine.close_spider(
                self,'no invalid param founded, please check the definition of RUN_PARAMS in seeting.py')


    def start_requests(self):
        keyword = self.searchParams[0]['keyword']
        max_page = self.searchParams[0]['maxPage']
        yield scrapy.Request(url=self.baseUrl.format(
            keyword=keyword,
            maxpage=max_page),
            callback=self.searchParse, meta={'keyword': keyword})

    def searchParse(self, response):
        keyword = response.meta['keyword']
        html = json.loads(response.body)
        node_list = html["data"]['result']
        for node in node_list[:1]:
            item = BilibiliVideoItem()
            item['keyword'] = keyword
            item['title'] = node['title'].replace('<em class="keyword">', '').replace('</em>', '')
            item['arcUrl'] = node['arcurl']
            self.log.debug(item['arcUrl'])
            yield scrapy.Request(url=item['arcUrl'], headers=SEARCH_HEADERS,
                                 meta={'item':item}, callback=self.downloadParse)


    def downloadParse(self, response):
        # 接收传递的item
        item = response.meta['item']
        pattern = '.__playinfo__=(.*)</script><script>window.__INITIAL_STATE__='
        infos = Selector(response).response.body_as_unicode()
        try:
            infos = re.findall(pattern, infos)[0]
            self.log.debug('.'.join(infos))
        except:
            return '', ''
        html = json.loads(infos)
        node_list = html['data']['dash']['video']
        baseUrl = node_list[0]['baseUrl']
        if 'mirrork' in baseUrl:
            item['oid'] = baseUrl.split('/')[6]
        else:
            id_ = baseUrl.split('/')[7]
            if len(id_) >= 10:
                id_ = baseUrl.split('/')[6]
            item['oid'] = id_

        download_urls = []
        for node in node_list:
            download_urls.append(node['baseUrl'])

        item['downloadUrls'] = download_urls
        item['status'] = 'start'
        yield item
