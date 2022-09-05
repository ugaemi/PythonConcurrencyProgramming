import asyncio
import os
import threading

import aiohttp
import time


async def fetcher(session, url):
    print(f"{os.getpid()} process | {threading.get_ident()} url : {url}")
    async with session.get(url, ssl=False) as response:
        return response.text


async def main():
    urls = ["https://naver.com", "https://apple.com"] * 20

    async with aiohttp.ClientSession() as session:
        result = await asyncio.gather(*[fetcher(session, url) for url in urls])


if __name__ == "__main__":
    start = time.time()
    asyncio.run(main())
    end = time.time()
    print(end - start)
