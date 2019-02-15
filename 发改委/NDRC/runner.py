# Scrapy运行程序
from scrapy.crawler import CrawlerProcess
from 发改委.NDRC.spiders.general import *
from scrapy.utils.project import get_project_settings


process = CrawlerProcess(get_project_settings())
# 导入 settings 设置（包括 pipeline）

process.crawl(GeneralSpider)

process.start()  # the script will block here until all crawling jobs are finished

