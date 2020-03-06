#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @description --


class Company(object):
    def __init__(self):
        self.id = None
        self.name = '-'
        self.representative = '-'
        self.address = '-'
        self.region = '-'
        self.city = '-'
        self.district = '-'
        self.biz_status = '-'
        self.credit_code = '-'
        self.email = '-'
        self.phone = '-'
        self.biz_scope = '-'
        self.company_type = '-'
        self.taxpayer_code = '-'
        self.registered_capital = '-'
        self.lat_long = '-'
        self.setup_time = '-'
        self.homepage = '-'
        self.register_code = '-'
        self.organization_code = '-'
        self.english_name = '-'
        self.authorization = '-'
        self.actual_capital = '-'
        self.industry = '-'
        self.used_name = '-'
        self.keyword = '-'

    def __str__(self) -> str:
        return "{}, {}".format(self.name, self.representative)

    def clear(self):
        self.__init__()


