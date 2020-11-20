import time
from selenium import webdriver
from unidecode import unidecode
from requests_html import HTMLSession
from bs4 import BeautifulSoup
import requests


def get_page_data():
    tic = time.perf_counter()
    url = 'https://wallex.ir/'
    browser = webdriver.PhantomJS()
    browser.get(url)
    html = browser.page_source
    soup = BeautifulSoup(html, 'lxml')
    prices = soup.find_all('strong')
    print('Tether elapse time {:.2f}'.format(time.perf_counter() - tic))
    return unidecode(prices[5].text)



def get_tether(session: HTMLSession):
    tic = time.perf_counter()
    print('Tether stated')
    url = 'https://wallex.ir/'
    r = session.get(url)
    r.html.render(timeout=50, sleep=0)
    price = r.html.find('strong')
    print('Tether elapse time {:.2f}'.format(time.perf_counter() - tic))
    return unidecode(price[5].text)


