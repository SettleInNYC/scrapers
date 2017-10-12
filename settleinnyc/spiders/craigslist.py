# -*- coding: utf-8 -*-
from datetime import datetime

import scrapy
from scrapy import Request
from scrapy_sqlitem import SqlSpider

from models import ListingItem


class Spider(SqlSpider):
    name = 'craigslist'
    allowed_domains = ['craigslist.org']
    start_urls = ['https://newyork.craigslist.org/search/aap']

    def parse(self, response):
        # The proxy middleware suggests this
        if not response.xpath('//a[@class="header-logo"]'):
            yield Request(url=response.url, dont_filter=True)

        # Find the results in the search with no terms and spawn other
        # requests
        for item in response.xpath('//p[@class="result-info"]'):
            relative_url = item.xpath('a/@href').extract_first()
            absolute_url = response.urljoin(relative_url)
            yield Request(absolute_url, callback=self.parse_item_page)

        relative_next_url = (response.xpath('//a[@class="button next"]/@href')
                             .extract_first())
        absolute_next_url = response.urljoin(relative_next_url)
        yield Request(absolute_next_url, callback=self.parse)

    def parse_item_page(self, response):
        price = (response.xpath('//span[@class="price"]/text()')
                 .extract_first())
        text = "".join(response
                       .xpath('//section[@id="postingbody"]/text()')
                       .extract())

        item = ListingItem()
        item['url'] =  response.url
        item['price'] = float(price.replace('$', ''))
        item['scraped_at'] = datetime.now()
        item['text'] = text
        yield item
