# 百度图像识别引擎，在发改委爬虫中未使用
from aip import AipOcr

config = {
    'appId': '11503474',
    'apiKey': 'V1ZyEwsZkjgwxQGmG14Y95g4',
    'secretKey': 'E9GzGYH0u9dgfQFXGTbLYqK0CEtHeWuf'
}

client = AipOcr(**config)


def get_file_content(file):
    with open(file, 'rb') as fp:
        return fp.read()


def img_to_str_local(image_path):
    image = get_file_content(image_path)
    result = client.basicGeneral(image)
    if 'words_result' in result:
        return '\n'.join([w['words'] for w in result['words_result']])


def img_to_str_net(url):
    result = client.basicGeneralUrl(url)
    if 'words_result' in result:
        return ' '.join([w['words'] for w in result['words_result']])
