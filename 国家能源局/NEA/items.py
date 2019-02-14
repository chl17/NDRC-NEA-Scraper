# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import MapCompose, TakeFirst
from scrapy.loader import ItemLoader                # 导入ItemLoader类也就加载items容器类填充数据
from 国家能源局.NEA.es_operation import *  # 导入elasticsearch操作模块
from elasticsearch_dsl.connections import connections       # 导入连接elasticsearch(搜索引擎)服务器方法
es_connection = connections.create_connection(hosts=['127.0.0.1'])


class NEAItemLoader(ItemLoader):
    default_output_processor = TakeFirst()


def addval(value):                                 # 自定义数据预处理函数
    return value                                    # 将处理后的数据返给Item


class NeaItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field(input_processor=MapCompose(addval))  # 接收爬虫获取到的title信息
    # author = scrapy.Field()
    date = scrapy.Field()
    year = scrapy.Field()
    month = scrapy.Field()
    day = scrapy.Field()
    url = scrapy.Field()
    image_urls = scrapy.Field()
    image_content = scrapy.Field()
    file_content = scrapy.Field()
    content = scrapy.Field()
    attachments = scrapy.Field()
    class0 = scrapy.Field()
    class1 = scrapy.Field()
    class2 = scrapy.Field()
    class3 = scrapy.Field()

    def save_to_es(self):
        nea_element = neaType()  # 实例化elasticsearch(搜索引擎对象)
        nea_element.title = self['title']  # 字段名称=值
        nea_element.content = self['content']
        nea_element.file_content = self['file_content']
        nea_element.image_content = self['image_content']
        nea_element.url = self['url']
        nea_element.date = self['date']
        nea_element.year = self['year']
        nea_element.month = self['month']
        nea_element.day = self['day']
        nea_element.attachments = self['attachments']
        nea_element.image_urls = self['image_urls']
        nea_element.class0 = self['class0']
        nea_element.class1 = self['class1']
        nea_element.class2 = self['class2']
        nea_element.class3 = self['class3']
        nea_element.suggest = gen_suggests(es_connection, neaType.name,
                                           ((nea_element.title, 10), (nea_element.file_content, 7),
                                            (nea_element.content, 8), (nea_element.image_content, 7)))  # neaType.Index.name
        nea_element.save()  # 将数据写入elasticsearch(搜索引擎对象)
        return
