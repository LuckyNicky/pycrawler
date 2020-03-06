#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import os
import pkg_resources
import semver
import locale, _locale
import atexit
import gettext

from scrapy.crawler import CrawlerProcess
from .utils.logger import getLogger
from .utils.misc import reversemap

__version__ = '0.0.1'
__version_info__ = semver.parse_version_info(__version__)

APPID = "pycrawler"
PKGDIR = pkg_resources.resource_filename(__name__, "")
RUNTIMEDIR = os.path.dirname(__file__) + os.sep.join(['','..','runtime',])

# Locale
locale.setlocale(locale.LC_ALL, "")
_locale._getdefaultlocale = lambda *args: ["en_US", "utf_8_sig"]

class Restart(Exception):
    __slots__ = []

class Exit(Exception):
    __slots__ = []

# TODO:
#  configurable system
class Core:
    LOCALE_DOMAIN = APPID
    DEBUG_LEVEL_MAP = {"debug": 1, "trace": 2, "stack": 3}

    @property
    def version(self):
        return __version__

    @property
    def version_info(self):
        return __version_info__

    @property
    def debug(self):
        return self._debug


    def __init__(self, debug=None):
        self._ = lambda x: x
        self._debug = 0
        self.rundir = RUNTIMEDIR
        self.crawler_proc = None
        self._init_config(debug)
        self._init_log()
        self._init_database()

        atexit.register(self.terminate)


    def _init_config(self, debug):
        from .config.parser import ConfigParser

        self.config = ConfigParser(self.rundir)
        if debug is None:
            if self.config.get("general", "debug_mode"):
                debug_level = self.config.get("general", "debug_level")
                self._debug = self.DEBUG_LEVEL_MAP[debug_level]
        else:
            self._debug = max(0, int(debug))

        self.config.save()  #: save so config file

    def _init_log(self):
        self.log = getLogger()

    def _init_database(self):
        pass


    def set_language(self, lang):
        localedir = os.path.join(PKGDIR, "locale")
        languages = (locale.locale_alias[lang.lower()].split("_", 1)[0],)
        self._set_language(self.LOCALE_DOMAIN, localedir, languages)

    def _set_language(self, *args, **kwargs):
        try:
            trans = gettext.translation(*args, **kwargs)
            try:
                self._ = trans.ugettext
            except AttributeError:
                self._ = trans.gettext
        except Exception:
            pass


    def _setup_language(self):
        self.log.debug("Setup language...")

        lang = self.config.get("general", "language")
        if not lang:
            lc = locale.getlocale()[0] or locale.getdefaultlocale()[0]
            lang = lc.split("_", 1)[0] if lc else "en"

        try:
            self.set_language(lang)
        except IOError as exc:
            self.log.warning(exc, exc_info=self.debug > 1, stack_info=self.debug > 2)
            self._set_language(self.LOCALE_DOMAIN, fallback=True)


    def _initScrapySettings(self, srcSettings):
        customSettings = srcSettings
        customSettings['FILES_STORE'] = os.sep.join([self.rundir, 'download'])

        return customSettings

    def start(self):
        try:
            self.log.debug("Starting core...")

            debug_level = reversemap(self.DEBUG_LEVEL_MAP)[self.debug].upper()
            self.log.debug(f"Debug level: {debug_level}")

            # self._setup_language()

            from .spiders.bilibiliSpider import BilibiliVideoSpider
            from .spiders.tianyanchaSpider import TianYaChaSpider
            from .spiders.shseSpider import QASpider
            spiders = [
                # BilibiliVideoSpider,
                # TianYaChaSpider,
                QASpider,
            ]

            self.log.debug('*******************run spider start...*******************')
            try:
                from scrapy.utils.project import get_project_settings
                settings = get_project_settings()
                self.crawler_proc = CrawlerProcess(
                    self._initScrapySettings(settings))
                for spider in spiders:
                    self.crawler_proc.crawl(spider, core=self)
                self.crawler_proc.start()
            except Exception as e:
                self.log.debug('[Error]# spider goes wroing.Return Message: {}'.format(str(e)))
                self.restart()

        except Restart:
            self.restart()

        except (Exit, KeyboardInterrupt, SystemExit):
            self.terminate()

        except Exception as exc:
            self.log.critical(exc, exc_info=True, stack_info=self.debug > 2)
            self.terminate()


    def restart(self):
        self.stop()
        self.log.info(self._("Restarting core..."))
        self.start()


    def terminate(self):
        self.stop()
        self.log.info(self._("Exiting core..."))

    def stop(self):
        try:
            self.log.debug("Stopping core...")

        finally:
            pass