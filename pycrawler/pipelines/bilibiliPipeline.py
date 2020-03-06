# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.pipelines.files import FilesPipeline
from scrapy.http import Request
import re, os
from urllib import parse

from ..settings import *
from ..utils.logger import getLogger
log = getLogger()


class BiliBiliDownloadPipeline(FilesPipeline):
    def get_media_requests(self, item, info):
        if info.spider.name in ['bilibili']:
            oid = item['oid'];
            urls = item['downloadUrls']
            filename = item['title']
            filename = re.sub(r'[☆❤◦？\\*|“<>:/()]', '', filename)
            for index in range(len(urls)):
                url = urls[index]
                if url != '' and oid != '':
                    download_headers = DOWNLOAD_HEADERS;
                    download_headers['Referer'] = \
                        download_headers['Referer'].format(keyword = parse.quote(item['keyword']))
                    yield Request(url, meta={'fileName': filename, 'fileNo': index}, headers=download_headers)

    def file_path(self, request, response=None, info=None):
        basedir = info.spider.core.rundir if info else '.'
        name = request.meta['fileName']
        num = request.meta['fileNo']
        dir_name = name
        file_name = name + str(num) + '.flv'
        path = os.sep.join([dir_name, file_name])
        return path

