import time
import random
import threading
import argparse
from queue import Queue
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import requests
from bs4 import BeautifulSoup
from nltk.tokenize import word_tokenize

from info_search.crawler_1.user_agents import ua_list


MIN_NUM_WORDS_PER_PAGE = 1000
PAGES_FOLDER = 'pages'
NUM_PAGES = 100


parser = argparse.ArgumentParser(
    prog='Crawler',
    description='Crawles specified web addresses recursively',
)
parser.add_argument(
    'addresses', metavar='A', type=str, nargs='+',
    help='a web address to be crawled'
)


class Page:
    def __init__(self, url, text):
        self.url = url
        self.text = text
        self.i = -1

    def __str__(self):
        return f"{self.i} - {self.url}"


def get_html(url: str) -> str:
    headers = {'User-Agent': random.choice(ua_list)}
    try:
        resp = requests.get(url, headers=headers)
        resp.encoding = resp.apparent_encoding
        return resp.text
    except Exception as e:
        print(e)
        return ''


def crawl_page(
        soup: BeautifulSoup,
        visited_urls: Queue,
        urls: Queue,
        base_url: str,
) -> None:
    link_elements = soup.select('a[href]')
    for link_element in link_elements:
        url = link_element['href']
        if url == '/':
            continue
        if not url.startswith(('https://', 'http://')):
            url = base_url + url
        if (
                url not in visited_urls.queue
                and url not in urls.queue
                and not url.startswith('javascript')
        ):
            urls.put(url)


def get_content(soup: BeautifulSoup, url: str, pages: Queue) -> bool:
    text = soup.get_text()
    tokenized = word_tokenize(text)
    if len(tokenized) > MIN_NUM_WORDS_PER_PAGE:
        pages.put(Page(url, text))
        return True
    return False


def download_pages(
        urls: Queue,
        visited_urls: Queue,
        pages: Queue,
        num_pages: int,
        lock: threading.Lock,
        base_url: str,
) -> int:
    while not urls.empty() and num_pages < NUM_PAGES:
        current_url = urls.get()
        visited_urls.put(current_url)
        print(current_url)
        soup = BeautifulSoup(get_html(current_url), 'html.parser')
        crawl_page(soup, visited_urls, urls, base_url)
        urls.task_done()
        if get_content(soup, current_url, pages):
            lock.acquire()
            num_pages += 1
            lock.release()
    return num_pages


def save_index(pages: Queue) -> None:
    path = Path('..', 'index.txt')
    with path.open(mode='w', encoding='utf-8') as f:
        f.writelines(map(
            lambda page: f"{PAGES_FOLDER}/{page.i}.txt {page.url}\n",
            pages.queue
        ))


def save_page(page: Page):
    path = Path('..', PAGES_FOLDER, str(page.i) + '.txt')
    with path.open(mode='w', encoding='utf-8') as f:
        f.write(page.text)


def save_pages(pages: Queue):
    folder = Path('..', PAGES_FOLDER)
    if not folder.is_dir():
        folder.mkdir()
    while not pages.empty():
        save_page(pages.get())


def run(addresses: [str]):
    urls = Queue()
    visited_urls = Queue()
    pages = Queue()
    lock = threading.Lock()
    num_pages = 0
    num_workers = 4
    address_i = 0
    while num_pages < NUM_PAGES:
        base_url = addresses[address_i]
        urls.put(base_url)
        with ThreadPoolExecutor(max_workers=num_workers) as executor:
            for _ in range(num_workers):
                downloader = executor.submit(
                    download_pages,
                    urls,
                    visited_urls,
                    pages,
                    num_pages,
                    lock,
                    base_url,
                )
                num_pages = downloader.result()
                print(num_pages)
        address_i += 1

    for i, page in enumerate(pages.queue):
        page.i = i

    save_index(pages)

    with ThreadPoolExecutor(max_workers=num_workers) as executor:
        for _ in range(num_workers):
            executor.submit(save_pages, pages)


if __name__ == '__main__':
    start_time = time.time()
    run(parser.parse_args().addresses)
    print("--- %s seconds ---" % (time.time() - start_time))
