import requests
from requests.utils import quote

from math import ceil


KEY = 'OB4BZ-D4W3U-B7VVO-4PJWW-6TKDJ-WPB77'
GET_URLS_FLAG = True
DetailUrlList = []
Headers = {
    'Referer': "https://lbs.qq.com/webservice_v1/guide-search.html",
    "Sec-Fetch-Mode": "no-cors",
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.87 Safari/537.36",
}
# DB_PARAMS = {
    # 'host': 'localhost', 'port': 3306, 'user': 'root', 'password': 'root1234', 'db': 'qmap', 'loop': event_loop
# }


def fetch(method, url, json_str=False, **kwargs):
    result = ''
    try:
        result = requests.request(method, url, **kwargs)
        result = result.text if not json_str else result.json()
    except Exception as e:
        result = e
    finally:
        return result


def get_province():
    '''获取全国城市信息'''
    url = 'https://apis.map.qq.com/ws/district/v1/x'
    headers = {
        'Accept': "*/*",
        'Host': "apis.map.qq.com",
        'Sec-Fetch-Mode': "no-cors",
        'Referer': "https://map.qq.com/",
        'User-Agent': "Mozilla/5.0 (MACintosh; Intel MAC OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.87 Safari/537.36",
        # 'Connection': "keep-alive",
    }
    params = {
        'method': 'city',
        'key': KEY
    }
    result = fetch('GET', url, params=params, headers=headers, json_str=True)
    province = result.get('detail').get('p')
    province.remove(province[0])
    return province


def get_data_by_city(prov: str='河北', city: str='北京', page: int=1, kw: str='游泳馆'):
    url = "https://apis.map.qq.com/ws/place/v1/search"
    querystring = {"boundary": quote(f"region({city}, 0)"), "keyword": kw, "page_size": "20",
        "page_index": str(page), "orderby": "_distance", "key": KEY
    }
    result = fetch('GET', url, params=querystring, headers=Headers, json_str=True)
    if result.get('status') != 0:
        print('exceed the limit')
        raise Exception(result.get('message'))
    if GET_URLS_FLAG:
        count = result.get('count')
        if count != 0:
            print(count)
        DetailUrlList.append([prov, city, count])
        print(f'got count: {count}')
        return 
    data = result.get('data')
    print('got data')
    # save(data)

def parse(data):
    ...

# def save(data):
#     async with aiomysql.create_pool(**DB_PARAMS)  as pool:
#         async with pool.get() as conn:
#             async with conn.cursor() as cur:
#                 sql = 'insert into '
#                 await cur.execute(sql)
#                 # value = await cur.fetchone()


def main():
    global GET_URLS_FLAG
    # 获取城市列表
    provinces = get_province()
    # 获取详细数据的urllist
    for x in provinces:
        prov = x.get('prov').get('fullName')
        print(f'prov: {prov}')
        for city in x.get('citys'):
            get_data_by_city(prov=prov, city=city, page=1)
    # 根据详细数据的urllist获取数据
    GET_URLS_FLAG = False
    get_data_task = []
    for prov, city, count in DetailUrlList:
        if not count:
            continue
        for x in range(1, ceil(count/20)):
            get_data_by_city(prov=prov, city=city, page=x)


if __name__ == "__main__":
    main()





