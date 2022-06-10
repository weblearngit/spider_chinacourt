# -*- coding: utf-8 -*-
"""
@desc: html的内容，保存为json，正文存到text中，目录为id
@version: python3
@author: shhx
@time: 2022/6/10 17:43

需要
item.id
item.content
"""
import os
import json
from .utils import mkdir_for_filepath


class ContentPipeline(object):
    def __init__(self, save_info):
        self.file_output_path = save_info["output_path"]
        self.content_min_length = save_info["content_min_length"]
        self.json_name = 'info.json'
        self.text_name = 'content.txt'

    @classmethod
    def from_crawler(cls, crawler):
        """
        获取spider的settings参数,返回Pipeline实例对象
        "CONTENT_SAVE_DIR": {
            "output_path": f"M:/z_corpus",
            "content_min_length": 300,
        },
        """
        save_info = crawler.settings["CONTENT_SAVE_DIR"]
        return cls(save_info)

    def process_item(self, item, spider):
        dir_name = item.get('id')
        if dir_name :
            dir_path = os.path.join(self.file_output_path, dir_name)
            json_path = os.path.join(dir_path, self.json_name)
            mkdir_for_filepath(json_path)
            open(json_path,'w',encoding='utf8').write(json.dumps(dict(item), ensure_ascii=False,indent=2))

            content_text = item.get('content')
            if content_text and len(content_text)>=self.content_min_length:
                open(os.path.join(dir_path, self.text_name),'w',encoding='utf8').write(content_text)
        return item
