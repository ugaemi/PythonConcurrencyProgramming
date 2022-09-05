import os
import threading
from concurrent.futures import ThreadPoolExecutor

import requests
import time


def fetcher(params):
    session, url = params[0], params[1]
    print(f"{os.getpid()} process | {threading.get_ident()} url : {url}")
    with session.get(url) as response:
        return response.text


def main():
    urls = ["https://naver.com", "https://apple.com"] * 20

    executor = ThreadPoolExecutor(max_workers=10)

    with requests.Session() as session:
        params = [(session, url) for url in urls]
        list(executor.map(fetcher, params))


if __name__ == "__main__":
    start = time.time()
    main()
    end = time.time()
    print(end - start)
