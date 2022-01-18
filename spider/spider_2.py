import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
from threading import Event
from messagequeue import Producer, Consumer
import simplejson

BASE_URL = 'https://news.cnblogs.com'
NEW_PAGE = '/n/page/'

headers = {
    'User-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36"
}


def starts_url(start, stop, step=1):
    p = Producer('192.168.66.12', 5672, 'guang', '123456', 'test', 'news', 'urls')
    for i in range(start, stop + 1, step):
        url = "{}{}{}/".format(BASE_URL, NEW_PAGE, i)
        print(url)
        p.produce(url)
    print('任务链接创建完成')


def crawler(e: Event):
    p = Producer('192.168.66.12', 5672, 'guang', '123456', 'test', 'news', 'htmls')
    c = Consumer('192.168.66.12', 5672, 'guang', '123456', 'test', 'news', 'urls')
    while not e.wait(1):
        url = c.consumer()
        if url:
            with requests.get(url, headers=headers) as response:
                if response.status_code == 200:
                    html = response.text
                    p.produce(html)


def parse(e: Event):
    p = Producer('192.168.66.12', 5672, 'guang', '123456', 'test', 'news', 'outputs')
    c = Consumer('192.168.66.12', 5672, 'guang', '123456', 'test', 'news', 'htmls')
    while not e.wait(1):
        html = c.consumer()
        if html:
            soup = BeautifulSoup(html, 'lxml')
            titles = soup.select('h2.news_entry > a')
            for title in titles:
                var = simplejson.dumps({
                    'title': title.text,
                    'url': BASE_URL + title.get('href', '')
                })
                p.produce(eval)


def persist(path, e: Event):
    c = Consumer('192.168.66.12', 5672, 'guang', '123456', 'test', 'news', 'outputs')
    with open(path, 'a+', encoding='utf8') as f:
        while not e.wait(1):
            data = c.consumer()
            print(data)
            if data:
                val = simplejson.loads(data)
                f.write("{}\x01{}\n".format(val['url'], val['title']))
                f.flush()


event = Event()
executor = ThreadPoolExecutor(10)
executor.submit(starts_url, 1, 2)
executor.submit(persist, 'news2.txt', event)

for i in range(5):
    executor.submit(crawler, event)
for i in range(4):
    executor.submit(parse, event)
