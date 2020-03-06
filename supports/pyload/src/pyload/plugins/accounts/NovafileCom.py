# -*- coding: utf-8 -*-

from ..base.xfs_account import XFSAccount


class NovafileCom(XFSAccount):
    __name__ = "NovafileCom"
    __type__ = "account"
    __version__ = "0.07"
    __status__ = "testing"

    __pyload_version__ = "0.5"

    __description__ = """Novafile.com account plugin"""
    __license__ = "GPLv3"
    __authors__ = [("Walter Purcaro", "vuolter@gmail.com")]

    PLUGIN_DOMAIN = "novafile.com"
