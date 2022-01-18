from queue import Queue
import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
from threading import Event

BASE_URL = "https://news.cnblogs.com"
NEWS_PAGE = "/n/page/"

headers = {
    'User-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36"
}

urls = Queue()
htmls = Queue()
outputs = Queue()


def starts_url(start, stop, step=1):
    """创建新闻urls,每页30条新闻"""
    for i in range(start, stop + 1, step):
        url = "{}{}{}/".format(BASE_URL, NEWS_PAGE, i)
        print(url)
        urls.put(url)
    print('任务链接创建完毕')


def crawler(e: Event):
    """爬取页面"""
    while not e.is_set():
        url = urls.get()
        with requests.get(url, headers=headers) as response:
            html = response.text
            htmls.put(html)


def parse(e: Event):
    """分析页面"""
    while not e.is_set():
        html = htmls.get()
        soup = BeautifulSoup(html, 'lxml')
        titles = soup.select('h2.news_entry > a')
        for title in titles:
            href = BASE_URL + title.get('href', '')
            txt = title.text
            val = href, txt
            outputs.put(val)


def persist(path, e:Event):
    """持久化"""
    with open(path, 'a+', encoding='utf8') as f:
        while not e.is_set():
            val = outputs.get()
            print(val)
            f.write('{}\x01{}\n'.format(val[0], val[1]))
            f.flush()


event = Event()
executor = ThreadPoolExecutor(10)
executor.submit(starts_url, 1, 1)
executor.submit(persist, 'news.txt', event)
for i in range(5):
    executor.submit(crawler, event)
for i in range(4):
    executor.submit(parse, event)
