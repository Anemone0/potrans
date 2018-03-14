#!/usr/bin/env python
# -*- coding=utf-8 -*-
import os
from multiprocessing import Pool
from contextlib import closing

import pytrans

BLOCK_SIZE = None
BLOCK_NUM = None
FILE_LINES_NUM = None


def adjust(readlines, pos):
    adjusted_pos = pos
    while not readlines[adjusted_pos].startswith("\n"):
        adjusted_pos += 1
    return adjusted_pos + 1


def write_to_file(readlines, _from, _to, filename):
    with open(filename, 'w') as f:
        for each in readlines[_from:_to]:
            f.write(each)


def split_file_by_pos(readlines, pos, filename):
    _from = 0
    _no = 1
    for each_pos in pos:
        write_to_file(readlines, _from, each_pos, filename + '_{}'.format(_no))
        _from = each_pos
        _no += 1
    write_to_file(readlines, _from, len(readlines), filename + '_{}'.format(_no))


def _reduce(filename, to_lang):
    _readlines = []
    for each_file_num in xrange(1, BLOCK_NUM + 1):
        with open(os.path.join(to_lang, filename + "_{}".format(each_file_num)), 'r') as f:
            _readlines += f.readlines()
    with open(filename[:-3] + "_reduce.po", 'w') as f:
        for each_line in _readlines:
            f.write(each_line)


def _map(filename, to_lang, email):
    for each_file_num in xrange(1, BLOCK_NUM + 1):
        part_filename = filename + "_{}".format(each_file_num)
        # print part_filename
        pytrans.TranPo(part_filename, to_lang, email)

def _tran(args):
    pytrans.TranPo(*args)

def _map_parallel(filename, to_lang, email):
    part_filenames = [("{0}_{1}".format(filename, num), to_lang, email) for num in xrange(1, BLOCK_NUM + 1)]

    with closing(Pool(processes=BLOCK_NUM)) as p:
        p.map(_tran, part_filenames)


def _parallelize(filename, _block_size=None, _block_num=None):
    global BLOCK_NUM
    global BLOCK_SIZE
    global FILE_LINES_NUM

    _readlines = []
    with open(filename, 'r') as f:
        _readlines = f.readlines()
    FILE_LINES_NUM = len(_readlines)

    if _block_num is not None:
        BLOCK_NUM = _block_num
        BLOCK_SIZE = FILE_LINES_NUM / BLOCK_NUM
    else:
        BLOCK_SIZE = _block_size
        BLOCK_NUM = FILE_LINES_NUM / BLOCK_SIZE

    pos = range(0, FILE_LINES_NUM, BLOCK_SIZE)
    pos = map(lambda e: adjust(_readlines, e), pos)
    BLOCK_NUM = len(pos) + 1
    split_file_by_pos(_readlines, pos, filename)


def main(filename, to_lang, email='test@test.com', _block_size=500, _block_num=None):
    _parallelize(filename, _block_size=_block_size, _block_num=_block_num)
    _map(filename, to_lang, email)
    _reduce(filename, to_lang)


if __name__ == '__main__':
    main('zh_CN.po', 'zh-CN')
