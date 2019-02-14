from datetime import datetime
from elasticsearch_dsl import Date, Nested, Boolean, \
    analyzer, Completion, Keyword, Text, Integer, Document, DocType

# 更多字段类型见第三百六十四节elasticsearch(搜索引擎)的mapping映射管理

from elasticsearch_dsl.connections import connections       # 导入连接elasticsearch(搜索引擎)服务器方法
connections.create_connection(hosts=['127.0.0.1'])


def gen_suggests(es_connection, index, info_tuple):  # info_tuple 元组
    es = es_connection
    # 根据字符串生成搜索建议数组
    used_words = set()
    # 去重以先来的为主
    suggests = []
    for text, weight in info_tuple:
        if text:
            # 调用es的analyze接口分析字符串：分词并做大小写的转换
            words = es.indices.analyze(index=index, params={'filter': ["lowercase"]},
                                       body={'text': text, 'analyzer': "ik_max_word"})
            analyzed_words = set([r["token"] for r in words["tokens"] if len(r["token"]) > 1])
            new_words = analyzed_words - used_words
        else:
            new_words = set()

        if new_words:
            suggests.append({"input": list(new_words), "weight": weight})

    return suggests


class neaType(Document):                                                   # 自定义一个类来继承DocType类
    # Text类型需要分词，所以需要知道中文分词器，ik_max_wordwei为中文分词器
    name = "国家能源局"
    title = Text(analyzer="ik_max_word")                                    # 设置，字段名称=字段类型，Text为字符串类型并且可以分词建立倒排索引
    content = Text(analyzer="ik_max_word")
    file_content = Text(analyzer="ik_max_word")
    image_content = Text(analyzer="ik_max_word")
    url = Keyword()                                                         # 设置，字段名称=字段类型，Keyword为普通字符串类型，不分词
    date = Date()                                   # 设置，字段名称=字段类型，Date日期类型
    year = Integer()
    month = Integer()
    day = Integer()
    image_urls = Keyword()
    attachments = Keyword()
    class0 = Keyword()
    class1 = Keyword()
    class2 = Keyword()
    class3 = Keyword()

    class Index:
        name = "国家能源局"                                                     # 设置索引名称(相当于数据库名称)


if __name__ == "__main__":          # 判断在本代码文件执行才执行里面的方法，其他页面调用的则不执行里面的方法
    neaType.init()                # 生成elasticsearch(搜索引擎)的索引，表，字段等信息
