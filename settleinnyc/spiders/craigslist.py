# -*- coding: utf-8 -*-
import re
import scrapy
from datetime import datetime
from scrapy import Request

KEYWORDS = [
    'no voucher',
    'no public assistance',
    'no program',
    'no public benefits'
]

KEYWORD_RES = map(lambda x: re.compile('\\b' + x + '\\b', re.I), KEYWORDS)


def extract_keywords(text):
    output = {}
    for keyword, pattern in zip(KEYWORDS, KEYWORD_RES):
        output[keyword] = bool(pattern.findall(text))
    return output


class Spider(scrapy.Spider):
    name = 'craigslist'
    allowed_domains = ['craigslist.org']
    start_urls = ['https://newyork.craigslist.org/search/aap']
    custom_settings = {
        'FEED_EXPORT_FIELDS': [
            'url', 'price', 'date',
            'no voucher',
            'no public assistance',
            'no public benefits',
        ]
    }

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
        data_row = {
            'url': response.url,
            'price': price,
            'date': datetime.now().isoformat(),
        }
        data_row.update(extract_keywords(text))
        yield data_row
