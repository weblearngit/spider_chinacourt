# -*- coding: utf-8 -*-
"""
@desc: html页面的内容
@version: python3
@author: shhx
@time: 2022/6/10 16:48
"""
import scrapy


class ContentItem(scrapy.Item):
    """
    html页面内容
    文本信息(只要站内链接的)，标题，日期(yyyyMMdd)，来源(网站名称)，URL，
    """

    id = scrapy.Field()
    url = scrapy.Field()
    title = scrapy.Field()
    issue_date = scrapy.Field()
    author = scrapy.Field()
    content = scrapy.Field()
    source = scrapy.Field()
    other_info = scrapy.Field()
