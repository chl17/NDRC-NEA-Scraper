# 爬虫 V1.0

## 框架

Scrapy

## 网站

1. 国家发改委
1. 国家能源局

* 均为所有版块

## 网页Rendering

* Splash（运行在Docker中）

网页中含有动态渲染内容（JavaScript等），需要完成渲染后再提取网页内容，也就是说在浏览器中观察到的动态渲染的部分实际上并不会在直接获取的网页源码中呈现，因此需要一个统一的渲染器（也即浏览器）处理动态渲染内容。

## 功能

### 主要功能

解析：

1. 网页内容（标题，正文，时间，作者，etc.）
1. 附件内容（docx,doc,xlsx,xls,pdf\)

并保存至数据库:

1. MongoDB（NoSQL数据库）
1. ElasticSearch（搜索引擎后端数据库）

### 细节

1. 增量爬取（已经爬取的不重复爬取，利用DeltaFetch库，使用Berkeley DB）
1. 使用百度AI平台对文件扫描件进行图像识别
1. 读取附件防阻塞，读取大型超过设定时间

# ElasticSearch搜索引擎

一个开源的分布式实时全文搜索引擎。

接受Scrapy写入数据时进行中文分词并根据文章标题、正文、附件内容生成搜索建议。

# ReactiveSearch

一个开源的ElasticSearch搜索引擎前端。

官方网站：[https://opensource.appbase.io/reactivesearch/](https://opensource.appbase.io/reactivesearch/)
[](https://github.com/appbaseio/reactivesearch)[https://github.com/appbaseio/reactivesearch](https://github.com/appbaseio/reactivesearch)

多种可自定义模块，包括搜索框，过滤器（日期、内容）等等，详情在官网和GitHub的介绍中


