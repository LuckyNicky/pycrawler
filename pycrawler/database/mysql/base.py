#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
# vim: set et sw=4 ts=4 sts=4 ff=unix fenc=utf8:
# Created on 2014-11-05 10:42:24

import MySQLdb.connections


class MySQLMixin(object):
    maxlimit = 18446744073709551615

    @property
    def dbcur(self):
        try:
            return self.conn.cursor()
        except (MySQLdb.connections.OperationalError, MySQLdb.connections.InterfaceError):
            self.conn.ping(reconnect=True)
            self.conn.database = self.database_name
            return self.conn.cursor()
