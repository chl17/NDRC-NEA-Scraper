from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search

es = Elasticsearch()

url0 = 'http://zfxxgk.nea.gov.cn/auto87/201803/t20180323_3131.htm'
url1 = 'http://www.ndrc.gov.cn/zwfwzx/tztg/201806/t20180614_889413.html'
url2 = ''
search = Search().using(es).query("match", url=url2)
if search:
    print(search)
