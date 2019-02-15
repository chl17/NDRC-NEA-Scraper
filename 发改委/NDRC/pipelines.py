# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo
from 发改委.NDRC.items import *
import datetime
from scrapy.pipelines.files import FilesPipeline
import scrapy
from scrapy.exceptions import DropItem
from scrapy.pipelines.images import ImagesPipeline
import re
from 发改委.NDRC.OCR import *
from 发改委.NDRC.utility import *
import func_timeout


class NdrcPipeline(object):

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),        # 从设置settings.py获取设置信息方法
            mongo_db=crawler.settings.get('MONGO_DB')
        )

    def open_spider(self, spider):      # 连接mongoDB
        CollectionName = '测试'  # + date_time
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]
        self.Collection = self.db[CollectionName]

    def process_item(self, item, spider):
        if isinstance(item, NdrcItem):
            data = dict(item)
            self.Collection.insert(data)        # 保存到 mongoDB
            item.save_to_es()                   # 保存到 es
            return item

    def close_spider(self, spider):
        self.client.close()             # 关闭mongoDB连接


class FilePipeline(FilesPipeline):      # 文件下载处理

    def file_path(self, request, response=None, info=None):
        item = request.meta['item']
        folder = item['title'].replace('(', '（').replace(' ', '_').replace(')', '）')
        folder_strip = strip(folder)
        folder_name = item['date'].replace('/', '-') + '_' + folder_strip
        file_guid = request.url.split('/')[-1]
        filename = u'/{0}/{1}'.format(folder_name, file_guid)
        return filename

    def item_completed(self, results, item, info):
        file_paths = [x['path'] for ok, x in results if ok]
        print(file_paths)
        if file_paths:
            item['file_content'] = readattachment(file_paths)
            # item['file_content'] = ' '.join(readattachment(file_paths))
        if not file_paths:
            print('File Downloaded Failed or No Attachment')
        return item

    def get_media_requests(self, item, info):
        if item['attachments']:
            for file_address in item['attachments']:
                referer = item['url']
                yield scrapy.Request(file_address, meta={'item': item, 'referer': referer})


class ImagePipeline(ImagesPipeline):        # 图像下载处理

    def file_path(self, request, response=None, info=None):
        item = request.meta['item']
        folder = item['title']
        folder_strip = strip(folder)
        folder_name = item['date'].replace('/', '-') + '_' + folder_strip
        file_guid = request.url.split('/')[-1]
        filename = u'/{0}/{1}'.format(folder_name, file_guid)
        return filename

    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem('Image Downloaded Failed or No Image')
        return item

    def get_media_requests(self, item, info):
        if item['image_urls']:
            for image_address in item['image_urls']:
                referer = item['url']
                yield scrapy.Request(image_address, meta={'item': item, 'referer': referer})


def strip(path):
    """
    :param path: 需要清洗的文件夹名字
    :return: 清洗掉Windows系统非法文件夹名字的字符串
    """
    path = re.sub(r'[？\\*|“<>:/]', '', str(path))
    return path
