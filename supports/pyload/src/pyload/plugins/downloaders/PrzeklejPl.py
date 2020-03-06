# -*- coding: utf-8 -*-

from ..base.dead_downloader import DeadDownloader


class PrzeklejPl(DeadDownloader):
    __name__ = "PrzeklejPl"
    __type__ = "downloader"
    __version__ = "0.16"
    __status__ = "stable"

    __pyload_version__ = "0.5"

    __pattern__ = r"http://(?:www\.)?przeklej\.pl/plik/.+"
    __config__ = []  # TODO: Remove in 0.6.x

    __description__ = """Przeklej.pl downloader plugin"""
    __license__ = "GPLv3"
    __authors__ = [("zoidberg", "zoidberg@mujmail.cz")]
