#/usr/bin/env python
#coding:utf-8
# Author        : tuxpy
# Email         : q8886888@qq.com.com
# Last modified : 2015-05-19 17:09:43
# Filename      : utils.py
# Description   : 
from __future__ import unicode_literals, print_function
import os

def get_tmp_filepath(_file):
    """生成一个针对_file的临时文件名"""
    _path = os.path.dirname(_file)
    _tmp_filename = os.path.basename(_file)

    if not _tmp_filename.startswith('.'):
        _tmp_filename = '.'  + _tmp_filename

    _tmp_filename += '_tmp'

    _tmp_filepath = os.path.join(_path, _tmp_filename)

    if os.path.exists(_tmp_filepath):
        return get_tmp_filepath(_tmp_filepath + '_1')

    return _tmp_filepath

