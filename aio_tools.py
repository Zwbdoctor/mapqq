import aiohttp

session = aiohttp.ClientSession()


class AioClient:

    async def fetch(self, method, url, result='text', **kwargs):
        resp = await session.request(method, url, **kwargs)
        assert resp.status == 200
        if result == 'text':
            return await resp.text()
        elif result == 'json':
            return await resp.json()

    async def set_async_pool(self, limit):
        global session
        await session.close()
        conn = aiohttp.TCPConnector(limit=limit)
        session = aiohttp.ClientSession(connector=conn)

    async def get(self, url, params=None, headers=None, verify=None, timeout=60, **kwargs):
        """
        Kwargs:
            result='text' or 'json'
        """
        try:
            return await self.fetch('GET', url, params=params, headers=headers, timeout=timeout, 
                                    **kwargs)
        except Exception as e:
            await self.tear_down()
            raise e

    async def post(self, url, data=None, params=None, headers=None, verify=None, timeout=60, **kwargs):
        try:
            return await self.fetch('POST', url, data=data, params=params, headers=headers, timeout=timeout, 
                                    **kwargs)
        except Exception as e:
            await self.tear_down()
            raise e

    async def tear_down(self):
        await session.close()
