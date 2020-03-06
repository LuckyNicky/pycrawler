# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class BilibiliVideoItem(scrapy.Item):
    keyword = scrapy.Field()
    title = scrapy.Field()
    arcUrl = scrapy.Field()
    downloadUrls = scrapy.Field()
    oid = scrapy.Field()
    status = scrapy.Field()
    
    

class TianYanChaCompanyItem(scrapy.Item):
    id = scrapy.Field()
    name = scrapy.Field()
    representative = scrapy.Field()
    address = scrapy.Field()
    region = scrapy.Field()
    city = scrapy.Field()
    district = scrapy.Field()
    biz_status = scrapy.Field()
    credit_code = scrapy.Field()
    email = scrapy.Field()
    phone = scrapy.Field()
    biz_scope = scrapy.Field()
    company_type = scrapy.Field()
    taxpayer_code = scrapy.Field()
    registered_capital = scrapy.Field()
    lat_long = scrapy.Field()
    setup_time = scrapy.Field()
    homepage = scrapy.Field()
    register_code = scrapy.Field()
    organization_code = scrapy.Field()
    english_name = scrapy.Field()
    authorization = scrapy.Field()
    actual_capital = scrapy.Field()
    industry = scrapy.Field()
    used_name = scrapy.Field()
    keyword = scrapy.Field()

    def update(self, company: dict):
        self.name = company.get('name', '-').replace('<em>', '').replace('</em>', '')
        self.representative = company.get('legalPersonName', '-')
        self.address = company.get('regLocation', '-')
        self.region = company.get('base', '-')
        self.city = company.get('city', '-')
        self.district = company.get('district', '-')
        self.biz_status = company.get('regStatus', '-')
        self.credit_code = company.get('creditCode', '-')
        self.email = company.get('emails', ['-']).split(';')[0].replace('\t', '')
        self.phone = company.get('phoneNum', '-')
        self.biz_scope = company.get('businessScope', '-')
        self.company_type = company.get('companyOrgType', '-').replace('\t', '')
        self.taxpayer_code = company.get('creditCode', '-')
        self.registered_capital = company.get('regCapital', '-')
        self.lat_long = str({
            'lat': company.get('latitude', '-'),
            'long': company.get('longitude', '-')
        })
        self.setup_time = company.get('estiblishTime', '-')[0:10]

    def update_detail(self, company_detail: dict):
        self.homepage = company_detail.get('websiteList', '-')
        self.register_code = company_detail.get('regNumber', '-')
        self.organization_code = company_detail.get('orgNumber', '-')
        self.english_name = company_detail.get('property3', '-')
        self.authorization = company_detail.get('regInstitute', '-')
        self.actual_capital = company_detail.get('actualCapital', '缺省')
        self.industry = company_detail.get('industry', '-')
        self.used_name = company_detail.get('historyNames', '-')

class QAItem(scrapy.Item):
    id = scrapy.Field()
    user_avatar = scrapy.Field()  # 头像
    user_name = scrapy.Field() #用户名
    company_name = scrapy.Field() #提问的公司名
    company_id = scrapy.Field() #公司ID
    question_time = scrapy.Field() #提问时间
    question_content = scrapy.Field() #提问内容
    answer_time = scrapy.Field() #回答时间
    answer_content = scrapy.Field() #回答内容