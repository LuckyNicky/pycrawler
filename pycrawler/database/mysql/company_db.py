#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
# vim: set et sw=4 ts=4 sts=4 ff=unix fenc=utf8:
# Created on 2014-10-13 22:02:57

import MySQLdb.connections

from .base import MySQLMixin
from ..basedb import BaseDB

class CompanyDB(MySQLMixin, BaseDB):
    __tablename__ = 'company'
    __createtable__ = '''CREATE TABLE IF NOT EXISTS %s (
    `id` int(11) unsigned not NULL AUTO_INCREMENT primary key COMMENT 'PK',
    `name` varchar(128) CHARACTER SET utf8mb4  NULL DEFAULT '-' COMMENT '公司名',
    `representative` varchar(40) CHARACTER SET utf8mb4  NULL DEFAULT '-' COMMENT '法人代表',
    `address` varchar(200) CHARACTER SET utf8mb4  NULL DEFAULT '-' COMMENT '公司地址',
    `region` varchar(15) CHARACTER SET utf8mb4  NULL DEFAULT '-' COMMENT '所属地区(省)',
    `city` varchar(15) character set utf8mb4  null default '-' COMMENT '城市',
    `district` varchar(15) character set utf8mb4  null default '-' COMMENT '区/县',
    `lat_long` varchar(80) character set utf8mb4  null default '-'COMMENT '经纬度，json -> {"lat": "30.18484477830133", "long": "120.06383340659741"}',
    `biz_status` varchar(20) CHARACTER SET utf8mb4  NULL DEFAULT '-' COMMENT '经营状态',
    `credit_code` varchar(32) CHARACTER SET utf8mb4  NULL DEFAULT '-' COMMENT '统一社会信用代码',
    `register_code` varchar(32) CHARACTER SET utf8mb4  NULL DEFAULT '-' COMMENT '注册号',
    `phone` varchar(20) CHARACTER SET utf8mb4  NULL DEFAULT '-' COMMENT '电话',
    `email` varchar(50) CHARACTER SET utf8mb4  NULL DEFAULT '-' COMMENT '邮箱',
    `setup_time` varchar(20)  NULL DEFAULT '-' COMMENT '成立时间',
    `industry` varchar(64) CHARACTER SET utf8mb4  NULL DEFAULT '-' COMMENT '所属行业',
    `biz_scope` varchar(1200) CHARACTER SET utf8mb4  NULL DEFAULT '-' COMMENT '经营范围',
    `company_type` varchar(32) CHARACTER SET utf8mb4  NULL DEFAULT '-' COMMENT '公司类型',
    `registered_capital` varchar(32) CHARACTER SET utf8mb4  NULL DEFAULT '-' COMMENT '注册资本',
    `actual_capital` varchar(32) CHARACTER SET utf8mb4  NULL DEFAULT '-' COMMENT '实缴资本',
    `taxpayer_code` varchar(32) CHARACTER SET utf8mb4  NULL DEFAULT '-' COMMENT '纳税人识别号',
    `organization_code` varchar(32) CHARACTER SET utf8mb4  NULL DEFAULT '-' COMMENT '组织机构代码',`english_name` varchar(128) CHARACTER SET utf8mb4  NULL DEFAULT '-' COMMENT '公司英文名',
    `authorization` varchar(64) CHARACTER SET utf8mb4  NULL DEFAULT '-' COMMENT '登记机关',
    `homepage` varchar(64) CHARACTER SET utf8mb4 NULL DEFAULT '-' COMMENT '公司官网',
    `used_name` varchar(500) CHARACTER SET utf8mb4  NULL DEFAULT '-' COMMENT '公司曾用名',
    `search_key` varchar(64) character set utf8mb4  null default '-' comment '搜索关键字',
    `create_at` timestamp not NULL DEFAULT CURRENT_TIMESTAMP COMMENT '插入时间',
    `modify_at` timestamp not NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '最后操作时间',
    unique key uq_credit_reg_code(`credit_code`, `register_code`)) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT '企业信息表' '''

    def __init__(self, host='192.168.98.10', port=3306, database='test_com',
                 user='test_com', passwd='123456'):

        self.database_name = database
        self.conn = MySQLdb.connect(
            user=user, password=passwd, database=database,
            host=host, port=port, autocommit=True)

        if database not in [x[0] for x in self._execute('show databases')]:
            self._execute('CREATE DATABASE %s' % self.escape(database))
        self._execute(self.__createtable__ % self.escape(self.__tablename__))

    def _parse(self, data):
        return data

    def _stringify(self, data):
        return data

    def save(self, data: dict):
        return self._replace(self.__tablename__, **self._stringify(data))

