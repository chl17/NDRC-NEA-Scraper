from scrapy.crawler import CrawlerProcess
from 国家能源局.NEA.spiders.general import *
from scrapy.utils.project import get_project_settings

# !!! 修改 scrapy.cfg
process = CrawlerProcess(get_project_settings())
# 导入 settings 设置（包括 pipeline）

process.crawl(GeneralSpider)

process.start()  # the script will block here until all crawling jobs are finished
