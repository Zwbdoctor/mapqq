import aiohttp

session = aiohttp.ClientSession()


class AioClient:

    result = None

    async def fetch(self, method, url, **kwargs):
        result_type = kwargs.get('result')
        async with session.request(method, url, **kwargs) as resp:
            if result_type == 'text':
                result = await resp.text()
                return result
            elif result_type == 'json':
                result = await resp.json()
                return result

    async def fetch_all(self, method, url, **kwargs):
        global session
        conn = aiohttp.TCPConnector(limit=5)
        session = aiohttp.ClientSession(connector=conn)
        return await self.fetch(method, url, **kwargs)

    async def get(self, url, params=None, headers=None, verify=None, timeout=60, result='text'):
        try:
            return await self.fetch('GET', url, params=params, headers=headers, verify=verify, timeout=timeout,
                                    result=result)
        except Exception as e:
            raise e
        finally:
            await self.tear_down()

    async def post(self, url, data=None, params=None, headers=None, verify=None, timeout=60, **kwargs):
        try:
            return await self.fetch('POST', url, data=data, params=params, headers=headers, verify=verify,
                                    timeout=timeout, **kwargs)
        except Exception as e:
            raise e
        finally:
            await self.tear_down()

    async def tear_down(self):
        await session.close()
