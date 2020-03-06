#!/usr/bin/env python

import unittest
import scrapy
from pycrawler.utils.logger import getLogger
log = getLogger()


class TestUtil(unittest.TestCase):

    def test_logger(self):
        log.debug('logger test')

    def test_download(self):
        pass


if __name__ == '__main__':
    unittest.main()
