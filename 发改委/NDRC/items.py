# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import MapCompose, TakeFirst
from scrapy.loader import ItemLoader                # 导入ItemLoader类也就加载items容器类填充数据
from 发改委.NDRC.es_operation import *             # 导入elasticsearch操作模块
from elasticsearch_dsl.connections import connections       # 导入连接elasticsearch(搜索引擎)服务器方法
es_connection = connections.create_connection(hosts=['127.0.0.1'])


class NDRCItemLoader(ItemLoader):
    default_output_processor = TakeFirst()


def addval(value):                                 # 自定义数据预处理函数
    return value                                    # 将处理后的数据返给Item


class NdrcItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field(input_processor=MapCompose(addval))  # 接收爬虫获取到的title信息 inputprocessor 处理数据后返回
    # author = scrapy.Field()
    date = scrapy.Field()
    year = scrapy.Field()
    month = scrapy.Field()
    day = scrapy.Field()
    url = scrapy.Field()
    image_urls = scrapy.Field()
    file_content = scrapy.Field()
    content = scrapy.Field()
    attachments = scrapy.Field()
    class0 = scrapy.Field()
    class1 = scrapy.Field()
    class2 = scrapy.Field()
    class3 = scrapy.Field()
    website = scrapy.Field()

    def save_to_es(self):
        ndrc_element = ndrcType()  # 实例化elasticsearch(搜索引擎对象)
        ndrc_element.title = self['title']  # 字段名称=值
        ndrc_element.content = self['content']
        ndrc_element.file_content = self['file_content']
        ndrc_element.url = self['url']
        ndrc_element.date = self['date']
        ndrc_element.year = self['year']
        ndrc_element.month = self['month']
        ndrc_element.day = self['day']
        ndrc_element.attachments = self['attachments']
        ndrc_element.image_urls = self['image_urls']
        ndrc_element.class0 = self['class0']
        ndrc_element.class1 = self['class1']
        ndrc_element.class2 = self['class2']
        ndrc_element.class3 = self['class3']
        ndrc_element.website = self['website']

        if self['file_content']:
            ndrc_element.suggest = gen_suggests(es_connection, ndrcType.name,
                                                ((ndrc_element.title, 10), (ndrc_element.file_content, 7),
                                                 (ndrc_element.content, 8)))  # ndrcType.Index.name
        else:
            ndrc_element.suggest = gen_suggests(es_connection, ndrcType.name,
                                                ((ndrc_element.title, 10), (ndrc_element.content, 8)))
        ndrc_element.save()  # 将数据写入elasticsearch(搜索引擎对象)
        print(self['title'])
        return
