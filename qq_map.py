import asyncio
from math import ceil
from requests.utils import quote
from aio_tools import AioClient

AC =  AioClient()
KEY = 'OB4BZ-D4W3U-B7VVO-4PJWW-6TKDJ-WPB77'
DetailUrlList = []
GET_URLS_FLAG = True
Headers = {
    'Referer': "https://lbs.qq.com",
    'User-Agent': "Mozilla/5.0 (MACintosh; Intel MAC OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.87 Safari/537.36",
}


async def get_province():
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
    result = await AC.get(url, params=params, headers=headers, verify=True, result='json')
    province = result.get('detail').get('p')
    province.remove(province[0])
    return province


async def get_data_by_city(prov: str='河北', city: str='北京', page: int=1):
    url = "https://apis.map.qq.com/ws/plACe/v1/search"
    querystring = {"boundary": quote(f"region({city}, 0)"), "keyword": "KFC", "page_size": "20",
        "page_index": str(page), "orderby": "_distance", "key": KEY
    }
    result = await AC.get(url, params=querystring, headers=Headers, result='json')
    if result.get('status') == 0:
        raise result.get('message')
    if GET_URLS_FLAG:
        count = result.get('count')
        DetailUrlList.append([prov, city, count])
        return 
    data = result.get('data')
    await save(data)

def save(data):
    ...


async def main():
    global GET_URLS_FLAG
    # 获取城市列表
    provinces = await get_province()
    # 获取详细数据的urllist
    url_tasks = []
    for x in provinces:
        prov = x.get('prov').get('fullName')
        for city in x.get('citys'):
            future = asyncio.ensure_future(get_data_by_city(prov=prov, city=city))
            url_tasks.append(future)
    await asyncio.wait(url_tasks)
    # 根据详细数据的urllist获取数据
    GET_URLS_FLAG = False
    get_data_task = []
    for prov, city, count in DetailUrlList:
        for x in range(1, ceil(count/20)):
            get_data_task.append(asyncio.ensure_future(get_data_by_city(prov=prov, city=city, page=x)))
    await asyncio.wait(get_data_task)
    


if __name__ == "__main__":
    event_loop = asyncio.get_event_loop()
    event_loop.run_until_complete(main())
