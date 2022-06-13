# -*- coding: utf-8 -*-
"""
@desc:
@version: python3
@author: shhx
@time: 2022/6/10 17:44
"""
import os


def mkdir_for_filepath(file_path):
    save_dir = os.path.dirname(file_path)
    if not os.path.isdir(save_dir):
        os.makedirs(save_dir)
