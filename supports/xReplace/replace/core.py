#/usr/bin/env python
#coding:utf-8
# Author        : tuxpy
# Email         : q8886888@qq.com.com
# Last modified : 2015-05-19 14:04:03
# Filename      : core.py
# Description   : 
from __future__ import unicode_literals, print_function
import os
from replace.filefilter import FileFilter
from replace.utils import get_tmp_filepath
import re
import signal

def exit_flush(func):
    def wrap(self, *args, **kwargs):
        signal.signal(signal.SIGINT, self.finished)
        signal.signal(signal.SIGTERM, self.finished)
        return func(self, *args, **kwargs)

    return wrap

def move_file(s_file, d_file):
    os.rename(s_file, d_file)

def del_file(s_file):
    try:
        os.remove(s_file)
    except OSError:
        pass

class FilesManager(object):
    tmp_files_list = []
    def __init__(self, target_path = None, filter_filename= None, is_filter = True, 
            source_re_string = None, target_string = None,
            include_hidden = False, interactive = False):
        self.target_path = target_path or os.getcwd() # 如果没有指定路径，则是自己当前工作路径
        self.file_filter = FileFilter(filter_filename = filter_filename, 
                is_filter = is_filter, include_hidden = include_hidden)
        self.source_re_string = source_re_string
        self.target_string = target_string
        self.interactive = interactive # 是否交互式替换

    @exit_flush
    def list_all_files(self):
        if os.path.isfile(self.target_path): # 如果目标是个文件，则直接返回
            yield self.target_path

        for root, dirs, files in os.walk(self.target_path):
            for _file in files:
                _file = os.path.join(root, _file)
                if not self.file_filter.file_is_filter(_file):
                    yield _file

    def all_replace(self, source_re_string = None, target_string = None):
        source_re_string = source_re_string or self.source_re_string
        target_string = target_string  or self.target_string

        assert source_re_string != None and target_string != None

        source_re = self.__compile_re(source_re_string)

        for _file in self.list_all_files():
            self.__replace_file(_file, source_re, target_string)

        self.flush_tmp()

    def __compile_re(self, re_string):
        return re.compile(re_string)

    def __replace_file(self, _file, 
            source_re, target_string):
        _source_fd = open(_file, 'rb')
        _tmp_filepath = get_tmp_filepath(_file)
        self.tmp_files_list.append(_tmp_filepath) # 组成一个临时文件名的列表，最后要对这里面的文件做删除工作
        _tmp_fd = open(_tmp_filepath, 'wb')

        for line_num, source_line in enumerate(_source_fd, 1):
            target_line = source_re.sub(target_string, source_line)
            if source_re.search(source_line):
                print(b"{file} : {line_num} line: {source_line} -> {target_line}".format(
                    file = _file, line_num = line_num, source_line = source_line.strip(), target_line = target_line.strip())) # 输入替换日志

                if self.interactive and raw_input('is replace(y or other): ').strip() not in ('y', 'Y'):
                    target_line = source_line

            _tmp_fd.write(target_line) # 先把文件写到一个缓存临时文件中去

        _source_fd.close()
        _tmp_fd.close()

        move_file(_tmp_filepath, _file)

    def flush_tmp(self):
        """清空缓存文件"""
        while self.tmp_files_list:
            _tmp_file = self.tmp_files_list.pop()
            if _tmp_file:
                del_file(_tmp_file)
            else:
                break

    def finished(self, sign_num, _):
        self.flush_tmp()
        print('\nbye~')
        import sys
        sys.exit()


