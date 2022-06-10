# -*- coding: utf-8 -*-
"""
   md5加密
"""
import hashlib
import os
import datetime
import time


def check_modified_time(filepath, diff_second=5 * 60):
    """
    判断文件的最后修改时间是否大于某个值
    :param filepath:
    :param diff_second:
    :return:
    """
    # 文件的最后修改时间
    file_stat = datetime.datetime.fromtimestamp(
        time.mktime(time.localtime(os.stat(filepath).st_mtime))
    )
    # 当前时间
    now = datetime.datetime.fromtimestamp(
        time.mktime(time.localtime(time.time()))
    )
    return (now - file_stat).seconds > diff_second


def cal_md5(obj, encoding="utf-8", isUpper=False):
    """
    # 计算传入对象的md5值
    # 先将传入对象做str()处理，再计算
    """
    # logger.debug(f"obj:{obj}")
    md5_str = hashlib.md5(str(obj).encode(encoding)).hexdigest()
    if isUpper:
        return md5_str.upper()
    else:
        return md5_str


def cal_md5_with_salt(src, salt, encoding="utf-8", isUpper=False):
    """
    原始数据拼接salt，然后计算md5
    """
    return cal_md5(src + salt, encoding=encoding, isUpper=isUpper)


def get_file_md5(filename, isUpper=False):
    """
    获取大文件的md5值
    :param filename:
    :param isUpper:
    :return:
    """
    if not os.path.isfile(filename):
        return
    d5 = hashlib.md5()
    with open(filename, "rb") as f:
        while True:
            b = f.read(8096)
            if not b:
                break
            d5.update(b)
    md5_str = d5.hexdigest()
    if isUpper:
        return md5_str.upper()
    else:
        return md5_str
