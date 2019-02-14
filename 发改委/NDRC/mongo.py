import pymongo
from datetime import *
# 读取一个 collection 中所有 content 和 file_content 组合输出string
# 最后重命名 collection

now = datetime.now()
date_time = now.strftime("%Y-%m-%d %H:%M:%S")


def readcontentstring(collection0):
    # mongodb服务的地址和端口号
    mongo_url = "127.0.0.1:27017"

    # 连接到mongodb，如果参数不填，默认为“localhost:27017”
    client = pymongo.MongoClient(mongo_url)

    # 连接到数据库
    DATABASE = "NEA"
    db = client[DATABASE]

    # 连接到集合(表):myDatabase.myCollection
    db_coll = db[collection0]

    result = db_coll.find()
    list0 = []
    for record in result:
        for contentline in record['content']:
            list0.append(contentline)
        if record['file_content']:
            for imagecontentline in record['file_content']:
                list0.append(imagecontentline)
    if list0:
        return '\n'.join(str(s) for s in list0 if s not in [None])  # 太强了！ join 出错 ，排了一个小时


def readcontentstringtest(collection):
    # mongodb服务的地址和端口号
    mongo_url = "127.0.0.1:27017"

    # 连接到mongodb，如果参数不填，默认为“localhost:27017”
    client = pymongo.MongoClient(mongo_url)

    # 连接到数据库
    DATABASE = "NEA"
    db = client[DATABASE]

    # 连接到集合(表):myDatabase.myCollection
    db_coll = db[collection]

    result = db_coll.find()
    list0 = []
    for record in result:
        for contentline in record['content']:
            print(contentline)
        if record['file_content']:
            for imagecontentline in record['file_content']:
                print(imagecontentline)
    return '\n'.join(list0)


def renameall():
    mongo_url = "127.0.0.1:27017"
    client = pymongo.MongoClient(mongo_url)
    DATABASE = "NEA"
    db = client[DATABASE]
    db.能源要闻.rename('能源要闻 ' + date_time)
    db.局工作动态.rename('局工作动态 ' + date_time)
    db.派出机构.rename('派出机构 ' + date_time)
    db.最新文件.rename('最新文件 ' + date_time)
    db.通知.rename('通知 ' + date_time)
    db.公告.rename('公告 ' + date_time)


# coll = '最新文件2018-07-07 22:54:36'
# contentlist = readcontentstring(coll)
# print(contentlist)
