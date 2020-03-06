#/usr/bin/env python
#coding:utf-8
# Author        : tuxpy
# Email         : q8886888@qq.com.com
# Last modified : 2015-05-20 07:39:25
# Filename      : setup.py
# Description   : 

from distutils.core import setup
from replace import version

setup(
        name = 'replace',
        version = version,
        author = 'tuxpy',
        author_email = 'q8886888@qq.com',
        license = 'GPL3',
        description = 'Batch Replace file contents',
        packages = [
            'replace',
            ],
        scripts = ['bin/replace'],
        )

