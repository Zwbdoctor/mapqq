import asyncio
import aiohttp

session = aiohttp.ClientSession()


async def fetch(method, url, **kwargs):
    result = kwargs.get('result')
    async with session.request(method, url, **kwargs) as resp:
        if result == 'text':
            return await resp.text()
        elif result == 'json':
            return await resp.json()


async def get(url, params=None, headers=None, verify=None, timeout=60, result='text'):
    try:
        return await fetch('GET', url, params=params, headers=headers, verify=verify, timeout=timeout,
                           result=result)
    except Exception as e:
        raise e
    finally:
        tear_down()


async def post(self, url, data=None, params=None, headers=None, verify=None, timeout=60, **kwargs):
    try:
        return await self.fetch('POST', url, data=data, params=params, headers=headers, verify=verify,
                                timeout=timeout, **kwargs)
    except Exception as e:
        raise e
    finally:
        self.tear_down()


def tear_down():
    session.close()


def get_province():
    url = 'https://s.map.qq.com/jsonEditor/config/xpconfig/xpconfig.js'
