from selenium import webdriver
import datetime
import random
import time
from urllib import parse


# selenium版本要v2的，最新的（v3、v4）不支持phantomJS
driver = webdriver.PhantomJS('D:/Program Files/phantomjs/bin/phantomjs.exe')
driver.set_window_size(1280, 1024)

url = 'http://cn.bing.com/search?' + parse.urlencode({
    'q':'C罗'
})

driver.get(url)


def savepic():
    base_dir = 'E:/study/P22033/flask_demo/test/pic/'
    filename = '{}{:%Y%m%d%H%M%S}{:03}.png'.format(
        base_dir,
        datetime.datetime.now(),
        random.randint(1, 100)
    )
    driver.save_screenshot(filename)

savepic()

MAXPETRIES = 5

for i in range(MAXPETRIES):
    time.sleep(1)
    try:
        ele = driver.find_element_by_id('b_results')
        if not ele.is_displayed():
            print('display none')
            continue
        print('ok')
        savepic()
        break
    except Exception as e:
        print(e)

driver.quit()
