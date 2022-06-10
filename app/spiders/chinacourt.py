# -*- coding: utf-8 -*-
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from apputils.yw_common import get_now_filename


def get_settings(name):
    settings = {
        "DOWNLOADER_MIDDLEWARES": {
            # "app.middlewares.proxy_request.ProxyMiddleware": 125,
        },
        "ITEM_PIPELINES": {"app.pipelines.file_save.TxtPipeline": 1},
        "TXT_SAVE": {
            "output_path": f"E:/Z_ES_DATA/{name}-{get_now_filename()}.txt",
            "flush_data_length": 100,
        },
        "DOWNLOAD_TIMEOUT": 20,
    }
    return settings


class ChinacourtSpider(CrawlSpider):
    name = "chinacourt"
    allowed_domains = ["www.chinacourt.org"]
    start_urls = ["http://www.chinacourt.org/"]

    custom_settings = get_settings(name)

    rules = (
        # 先抓取全部url，之后针对性过滤
        Rule(LinkExtractor(allow=r"/.*"), callback="parse_item", follow=True),
    )

    def parse_item(self, response):
        row_dict = {"page_url": response.url}
        yield row_dict
