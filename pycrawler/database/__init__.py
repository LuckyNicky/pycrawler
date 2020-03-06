#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# vim: set et sw=4 ts=4 sts=4 ff=unix fenc=utf8:
# Author: Binux<i@binux.me>
#         http://binux.me
# Created on 2014-10-08 15:04:08

from six.moves.urllib.parse import urlparse

def connect_database(url):
    """
    create database object by url

    mysql:
        mysql+type://user:passwd@host:port/database
    sqlite:
        # relative path
        sqlite+type:///path/to/database.db
        # absolute path
        sqlite+type:////path/to/database.db
        # memory database
        sqlite+type://
    mongodb:
        mongodb+type://[username:password@]host1[:port1][,host2[:port2],...[,hostN[:portN]]][/[database][?options]]
        more: http://docs.mongodb.org/manual/reference/connection-string/
    sqlalchemy:
        sqlalchemy+postgresql+type://user:passwd@host:port/database
        sqlalchemy+mysql+mysqlconnector+type://user:passwd@host:port/database
        more: http://docs.sqlalchemy.org/en/rel_0_9/core/engines.html
    redis:
        redis+taskdb://host:port/db
    elasticsearch:
        elasticsearch+type://host:port/?index=pyspider
    couchdb:
        couchdb+type://[username:password@]host[:port]
    local:
        local+projectdb://filepath,filepath

    type:
        taskdb
        projectdb
        resultdb

    """
    db = _connect_database(url)
    db.copy = lambda: _connect_database(url)
    return db


def _connect_database(url):  # NOQA
    parsed = urlparse(url)

    scheme = parsed.scheme.split('+')
    if len(scheme) == 1:
        raise Exception('wrong scheme format: %s' % parsed.scheme)
    else:
        engine, dbtype = scheme[0], scheme[-1]
        other_scheme = "+".join(scheme[1:-1])

    if engine == 'mysql':
        return _connect_mysql(parsed, dbtype)
    elif engine == 'sqlite':
        return _connect_sqlite(parsed, dbtype)
    elif engine == 'mongodb':
        return _connect_mongodb(parsed, dbtype, url)
    elif engine == 'redis':
        return _connect_redis(parsed, dbtype)
    else:
        raise Exception('unknown engine: %s' % engine)


def _connect_mysql(parsed, dbtype):
    parames = {}

    if parsed.username:
        parames['user'] = parsed.username
    if parsed.password:
        parames['passwd'] = parsed.password
    if parsed.hostname:
        parames['host'] = parsed.hostname
    if parsed.port:
        parames['port'] = parsed.port
    if parsed.path.strip('/'):
        parames['database'] = parsed.path.strip('/')

    if dbtype == 'tianyanchadb':
        from .mysql.company_db import CompanyDB
        return CompanyDB(**parames)
    if dbtype == 'qadb':
        from .mysql.qa_db import QuestionAnswerDB
        print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>.\n')
        return QuestionAnswerDB(**parames)
    else:
        raise LookupError('mysql not supported dbtype: %s' % dbtype)



def _connect_sqlite(parsed, dbtype):
    if parsed.path.startswith('//'):
        path = '/' + parsed.path.strip('/')
    elif parsed.path.startswith('/'):
        path = './' + parsed.path.strip('/')
    elif not parsed.path:
        path = ':memory:'
    else:
        raise Exception('error path: %s' % parsed.path)

    if False:
        pass
    else:
        raise LookupError('sqlite not supported dbtype: %s' % dbtype)


def _connect_mongodb(parsed, dbtype, url):
    url = url.replace(parsed.scheme, 'mongodb')
    parames = {}
    if parsed.path.strip('/'):
        parames['database'] = parsed.path.strip('/')

    if False:
        pass
    else:
        raise LookupError('mongodb not supported dbtype: %s' % dbtype)


def _connect_redis(parsed, dbtype):
    parames = {}

    if parsed.hostname:
        parames['host'] = parsed.hostname
    if parsed.port:
        parames['port'] = parsed.port
    parames['database'] = int(parsed.path.strip('/')  or 0);

    if False:
        pass
    else:
        raise LookupError('redis not supported dbtype: %s' % dbtype)