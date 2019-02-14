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


# print(type(img_to_str_net('http://zfxxgk.nea.gov.cn/auto93/201806/W020180629331250434030.jpg')))
# print(img_to_str('/Users/chenhaolin/PycharmProjects/SRT/IMAGES/full/国家能源局_first 国务院扶贫办关于下达十三五”第一批光伏扶贫项目计划的通知/W020180104619948696131.jpg'))

