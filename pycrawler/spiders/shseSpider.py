# -*- coding:utf-8 -*-
from scrapy import Spider

from scrapy.http import Request
from ..items import QAItem

class QASpider(Spider):
    name = 'shse'
    allowed_domains = ['sseinfo.com']
    start_urls=['http://sns.sseinfo.com/ajax/feeds.do?type=11&pageSize=10&lastid=-1&show=1&page=1']
    page = 1;

    def parse(self, response):
        sel = response.xpath('//*[@class="m_feed_item"]')
        for s in sel:
            item = QAItem()
            item['id'] = s.xpath('./@id').extract_first().strip().split('-')[-1]
            item['user_avatar'] = s.xpath('./div[@class="m_feed_detail m_qa_detail"]/div[@class="m_feed_face"]/a/img/@src').extract_first().strip()
            item['user_name'] = s.xpath('./div[@class="m_feed_detail m_qa_detail"]/div[@class="m_feed_face"]/p/text()').extract_first().strip()
            company = s.xpath('./div[@class="m_feed_detail m_qa_detail"]/div[@class="m_feed_cnt "]/div[@class="m_feed_txt"]/a/text()').extract_first().strip()
            company_split = company.split('(')
            item['company_name'] = company_split[0].replace(':', '')
            item['company_id'] = company_split[1].replace(')', '')
            item['question_time'] = s.xpath('./div[@class="m_feed_detail m_qa_detail"]/div[@class="m_feed_cnt "]/div[@class="m_feed_func"]/div[@class="m_feed_from"]/span/text()').extract_first().strip()
            item['question_content'] = s.xpath('./div[@class="m_feed_detail m_qa_detail"]/div[@class="m_feed_cnt "]/div[@class="m_feed_txt"]/text()').extract()[1].strip()
            item['answer_time'] = s.xpath('./div[@class="m_feed_detail m_qa"]/div[@class="m_feed_func top10"]/div[@class="m_feed_from"]/span/text()').extract_first().strip()
            item['answer_content'] = s.xpath('./div[@class="m_feed_detail m_qa"]/div[@class="m_feed_cnt"]/div[@class="m_feed_txt"]/text()').extract_first().strip()
            yield item

        self.page += 1;
        next_url = 'http://sns.sseinfo.com/ajax/feeds.do?type=11&pageSize=10&lastid=-1&show=1&page=' + str(self.page)
        yield Request(next_url, callback=self.parse)
        

        