# -*- coding: utf-8 -*-
# AUTHOR: vuolter

from loguru import logger
import os, datetime

LOG_DIR = os.path.dirname(__file__) + os.sep.join(['','..','..','runtime',])
LOG_EXTENSION = ".log"
LOG_CONFIG = {
    'enqueue':True,
    'rotation':"500 MB",
}

class LogggerFactory:

    def __init__(self):
        self.config = {}
        self.loggers = {}

    def get_logger(self, name=None, **kwargs):
        _logger = None;
        log_dir = LOG_DIR

        self.config.clear()
        self.config.update(LOG_CONFIG)
        for key, value in kwargs.items():
            self.config[key] = value
        if name == 'console':
            pass
        else:
            log_name = 'runtime-{}'.format(datetime.date.today())
            if not name:
                self.config['retention'] = '1 days'
            else:
                log_name = name

            _logger = logger.add(
                os.sep.join([log_dir, 'logs', log_name+LOG_EXTENSION]), **self.config)

        self.loggers[name] = _logger

        return logger

logger_fac = LogggerFactory()
getLogger = logger_fac.get_logger