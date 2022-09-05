import os
import threading

import requests
import time


def fetcher(session, url):
    print(f"{os.getpid()} process | {threading.get_ident()} url : {url}")
    with session.get(url) as response:
        return response.text


def main():
    urls = ["https://naver.com", "https://apple.com"] * 20

    with requests.Session() as session:
        result = [fetcher(session, url) for url in urls]


if __name__ == "__main__":
    start = time.time()
    main()
    end = time.time()
    print(end - start)
