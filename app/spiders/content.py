# -*- coding: utf-8 -*-
import scrapy
import json
from pyquery import PyQuery as pq
from app.items.html_content import ContentItem
from .web_url_utils import get_url_md5
from .time_str import format_rq_str



def get_settings(name):
    settings = {
        "DOWNLOADER_MIDDLEWARES": {
            # "app.middlewares.proxy_request.ProxyMiddleware": 125,
        },
        "ITEM_PIPELINES": {"app.pipelines.html_text_json.ContentPipeline": 1},
        "CONTENT_SAVE_DIR": {
            "output_path": f"./output-{name}",
            "content_min_length": 100,
        },
    }
    return settings


class ContentSpider(scrapy.Spider):
    name = "content"
    allowed_domains = ["www.chinacourt.org"]
    spider_source = "www.chinacourt.org"

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'
    }

    custom_settings = get_settings(name)

    def start_requests(self):
        urls = [
            "https://www.chinacourt.org/index.shtml",
            "https://www.chinacourt.org/article/detail/2022/05/id/6706278.shtml",
            "https://www.chinacourt.org/article/detail/2022/06/id/6731932.shtml",
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse, headers=self.headers)

    def parse(self, response):
        item_dict = {
            "id": get_url_md5(response.url),
            "url": response.url,
            "source": self.spider_source,
            "title": "",
            "author": "",
            "issue_date": "",
            "content": "",
        }
        other_info = {}

        doc = pq(response.text)

        # 标题
        css_selector = "div[class=detail_bigtitle]"
        if doc.find(css_selector):
            item_dict['title'] = doc(css_selector).text()

        # 发布时间、发布人
        css_selector = "div[class=detail_thr]"
        if doc.find(css_selector):
            item_dict['author'] = doc(css_selector).text()
        if item_dict['author']:
            rq_str = format_rq_str(item_dict['author'])
            if rq_str:
                item_dict['issue_date'] = rq_str.replace("-", "")

        # 正文
        css_selector = "div[class=detail_txt]"
        if doc.find(css_selector):
            item_dict['content'] = doc(css_selector).text()

        # 网站上的导航
        css_selector = "div[class=address]"
        if doc.find(css_selector):
            other_info['address'] = doc(css_selector).text()

        item_dict['other_info'] = json.dumps(other_info,ensure_ascii=False)
        yield ContentItem(**item_dict)
