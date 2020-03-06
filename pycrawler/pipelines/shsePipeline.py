# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

from ..database import connect_database

from ..utils.logger import getLogger
log = getLogger()


class ShseDbPipeline(object):
    def __init__(self):
        self.db = connect_database('mysql+qadb://192.168.98.10/test_com')

    def open_spider(self, spider):
        """This method is called when the spider is opened."""
        log.info('open spider')

    def process_item(self, item, spider):
        """process news item"""
        if spider.name in ['shse']:
            self.db.save(data=dict(item))

        return item


