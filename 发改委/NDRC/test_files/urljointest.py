from urllib.parse import urlsplit
from urllib.parse import urljoin
doc = 'http://tzs.ndrc.gov.cn/zytzxmzbglbf0607.pdf'
html = 'http://www.ndrc.gov.cn/yjzx/yjzx_add.jsp?SiteId=149'
complete = urljoin(html, doc)
print(complete + '\n')

split = urlsplit('http://www.ndrc.gov.cn/zwfwzx/zfdj/jggg/', )
for i in range(4):
    print(split[i])

