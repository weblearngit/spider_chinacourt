# -*- coding: utf-8 -*-
"""
@desc:
@version: python3
@author: shhx
@time: 2020-02-21 15:23
"""
from urllib.parse import urlparse, urlencode, parse_qsl, urlsplit
from .md5 import cal_md5


def build_url_with_params(base_url, params):
    """
    将参数拼接到url上
    :param base_url:
    :param params: dict
    :return:
    """
    if not isinstance(params, dict):
        params = {}
    obj = urlparse(base_url)
    t_params = dict(parse_qsl(obj.query))
    t_params.update(params)
    url = f"{obj.scheme}://{obj.netloc}{obj.path}" + "?" + urlencode(t_params)
    return url


def get_url_md5(url):
    """
    获取url的md5，用于id
    :param url:
    :return:
    """
    url_part = urlsplit(url)
    url_str = "/".join([url_part.netloc, url_part.path.strip("/")])
    return cal_md5(url_str)
