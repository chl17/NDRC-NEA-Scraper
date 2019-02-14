# -*- coding: utf-8 -*-
import scrapy
from 发改委.NDRC.items import NdrcItem
from 发改委.NDRC.date import *
from 发改委.NDRC.utility import *
from scrapy_splash import SplashRequest
global count
count = 0


class GeneralSpider(scrapy.Spider):
    name = "NDRC_general"
    allowed_domains = ['ndrc.gov.cn']
    start_urls = [
        'http://www.ndrc.gov.cn/zwfwzx/tztg/',  # 政务服务中心>通知通告
    ]

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url, callback=self.parse)

    def parse(self, response):
        linklist_raw = response.xpath('//div//div//li//a/@href').extract()
        linklist = []
        for link in linklist_raw:
            linklist.append(response.urljoin(link))
        datelist = response.xpath('//font[@class="date"]/text()').extract()
        for i in range(len(linklist)):
            yield scrapy.Request(url=linklist[i], callback=self.parse_content, dont_filter=True, meta={'date': datelist[i]})

        next = response.xpath('//li//a[text()="下一页"]/@href').extract_first()
        global count
        if next and count < 2:
            yield scrapy.Request(url=next, callback=self.parse, dont_filter=True)
            count += 1

    def parse_content(self, response):
        if response.xpath('//div[@class="txt_title1 tleft"]/text()').extract_first():
            title = response.xpath('//div[@class="txt_title1 tleft"]/text()').extract_first()
            date = response.meta['date']
            author = response.xpath('//span[@id="dSource"]//a/@title').extract_first()
            paralist = response.xpath('//*[@id="zoom"]//div//p/text()').extract()

            item = NdrcItem()
            item['attachments'] = []
            item['content'] = ['']
            item['image_urls'] = []
            item['file_content'] = []
            item['author'] = author
            item['title'] = title
            item['date'] = date
            date_struct = datetime.datetime.strptime(date, "%Y/%m/%d")
            item['year'] = date_struct.year
            item['month'] = date_struct.month
            item['day'] = date_struct.day
            item['content'] = paralist
            item['url'] = response.url
            yield item
        elif response.xpath('//div[@class="tit2b "]/text()').extract_first():
            title = ''.join(response.xpath('//div[@class="tit2b "]/text()').extract())
            date = response.meta['date']
            paralist = response.xpath('//div[@class="txt1"]/text()').extract()

            item = NdrcItem()
            item['attachments'] = []
            item['image_urls'] = []
            item['file_content'] = []
            item['title'] = title
            item['date'] = date
            date_struct = datetime.datetime.strptime(date, "%Y/%m/%d")
            item['year'] = date_struct.year
            item['month'] = date_struct.month
            item['day'] = date_struct.day
            item['content'] = paralist
            item['arthor'] = ''
            item['url'] = response.url
            yield item
        elif response.xpath('//font[@style="font-size: 18pt"]/text()').extract_first():
            title = ''.join(response.xpath('//font[@style="font-size: 18pt"]/text()').extract())
            date = response.meta['date']
            paralist = response.xpath('//*[@id="zoom"]//div//p/text()').extract()

            item = NdrcItem()
            item['attachments'] = []
            item['image_urls'] = []
            item['file_content'] = []
            item['title'] = title
            item['date'] = date
            date_struct = datetime.datetime.strptime(date, "%Y/%m/%d")
            item['year'] = date_struct.year
            item['month'] = date_struct.month
            item['day'] = date_struct.day
            item['content'] = paralist
            item['arthor'] = response.xpath('//span[@id="dSourceText"]//@title').extract_first()
            item['url'] = response.url
            yield item
