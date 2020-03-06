# -*- coding: utf-8 -*-

from ..base.dead_downloader import DeadDownloader


class NahrajCz(DeadDownloader):
    __name__ = "NahrajCz"
    __type__ = "downloader"
    __version__ = "0.26"
    __status__ = "stable"

    __pyload_version__ = "0.5"

    __pattern__ = r"http://(?:www\.)?nahraj\.cz/content/download/.+"
    __config__ = []  # TODO: Remove in 0.6.x

    __description__ = """Nahraj.cz downloader plugin"""
    __license__ = "GPLv3"
    __authors__ = [("zoidberg", "zoidberg@mujmail.cz")]
