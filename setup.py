#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import sys
from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

import pycrawler

install_requires = [

    'scrapy']

if sys.version_info >= (3, 0):  # 3.*
    install_requires.extend([

    ])

extras_require_all = [

]
if sys.version_info >= (3, 0):  # 3.*
    extras_require_all.extend([

    ])


setup(
    name='pycrawler',
    version=pycrawler.__version__,

    description='A Powerful Web Crawler in Python',
    long_description=long_description,

    license='Apache License, Version 2.0',

    classifiers=[
        'Development Status :: 4 - Beta',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',

        'License :: OSI Approved :: Apache Software License',

        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Environment :: Web Environment',

        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],

    keywords='scrapy crawler spider webui',

    packages=find_packages(exclude=['data', 'tests*']),

    install_requires=install_requires,

    extras_require={
        'all': extras_require_all,
        'test': [
            'coverage',
            'httpbin<=0.5.0',
            'pyproxy==0.1.6',
            'easywebdav==1.2.0',
        ]
    },

    package_data={
        'pycrawler': [
            'logging.conf',
            'fetcher/phantomjs_fetcher.js',
            'fetcher/splash_fetcher.lua',
            'webui/static/*.js',
            'webui/static/*.css',
            'webui/templates/*'
        ],
    },

    entry_points={
        'console_scripts': [
            'pycrawler=pycrawler.run:main'
        ]
    },

    test_suite='tests.all_suite',
)
