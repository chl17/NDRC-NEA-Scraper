# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo
import datetime
from scrapy.pipelines.files import FilesPipeline
import scrapy
from scrapy.exceptions import DropItem
from scrapy.pipelines.images import ImagesPipeline
import re
import func_timeout
from 国家能源局.NEA.OCR import *
from 国家能源局.NEA.utility import *
from 国家能源局.NEA.items import *


class NeaPipeline(object):

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DB')
        )

    def open_spider(self, spider):

        CollectionName = '测试'  # + date_time
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]
        self.Collection = self.db[CollectionName]

    def process_item(self, item, spider):
        if isinstance(item, NeaItem):
            if item['image_urls']:
                for image_address in item['image_urls']:
                    content = img_to_str_net(image_address)
                    if content:
                        item['image_content'].append(content)
                item['image_content'] = ' '.join(item['image_content'])
            data = dict(item)
            self.Collection.insert(data)
            item.save_to_es()
            return item

    def close_spider(self, spider):
        self.client.close()


class FilePipeline(FilesPipeline):

    def file_path(self, request, response=None, info=None):
        item = request.meta['item']
        folder = item['title']
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
            raise DropItem('File Downloaded Failed or No Attachment')
        return item

    def get_media_requests(self, item, info):
        if item['attachments']:
            for file_address in item['attachments']:
                referer = item['url']
                yield scrapy.Request(file_address, meta={'item': item, 'referer': referer})


class ImagePipeline(ImagesPipeline):

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
