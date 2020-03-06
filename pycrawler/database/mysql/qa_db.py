#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
# vim: set et sw=4 ts=4 sts=4 ff=unix fenc=utf8:
# Created on 2014-10-13 22:02:57

import MySQLdb.connections

from .base import MySQLMixin
from ..basedb import BaseDB

class QuestionAnswerDB(MySQLMixin, BaseDB):
    __tablename__ = 'shse_qa'
    __createtable__ = '''CREATE TABLE IF NOT EXISTS %s (
    `id` int(11) unsigned not NULL primary key COMMENT 'PK',
    `current_time` timestamp not NULL DEFAULT CURRENT_TIMESTAMP COMMENT '插入时间',
    `user_name` VARCHAR(100) NOT NULL,
    `user_avatar` VARCHAR(255) NOT NULL,
    `company_name` VARCHAR(100) NOT NULL,
    `company_id` int(20) NOT NULL,
    `question_time` VARCHAR(100) NOT NULL,
    `question_content` text NOT NULL,
    `answer_time` VARCHAR(100),
    `answer_content` text
    )ENGINE=InnoDB DEFAULT CHARSET=utf8'''

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

