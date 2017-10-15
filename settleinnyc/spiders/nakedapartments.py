# -*- coding: utf-8 -*-
from datetime import datetime
from models import ListingItem
from scrapy import Request
from scrapy_sqlitem import SqlSpider
import scrapy
import re
import urlparse


class NakedapartmentsSpider(SqlSpider):
    name = 'nakedapartments'
    allowed_domains = ['www.nakedapartments.com']
    start_urls = ['http://www.nakedapartments.com/nyc/neighborhoods']

    def parse(self, response):
        neighborhood_links = response.xpath(
            '//div[@class="neighborhood-links"]//a/@href')
        for link in neighborhood_links.extract():
            yield Request(link, callback=self.parse_neighborhood_page)

    def parse_neighborhood_page(self, response):
        listing_links = response.xpath(
            '//a[@class="listing-row__image-link"]/@href')
        for link in listing_links.extract():
            yield Request(link, callback=self.parse_listing_page)
        next_page = response.xpath(
            '//*[@class="next_page"]/@href').extract_first()
        next_link = urlparse.urljoin(response.url, next_page)
        yield Request(next_link, callback=self.parse_neighborhood_page)

    def parse_listing_page(self, response):
        price = float(response.xpath('//*[@class="price"]/text()')
                      .extract_first()
                      .replace('$', '')
                      .replace(',', ''))
        text = re.sub('<[^>]+>', '', ''.join(
            response.css('.text').extract())).strip()
        item = ListingItem()
        item['url'] =  response.url
        item['price'] = price
        item['scraped_at'] = datetime.now()
        item['text'] = text
        yield item
