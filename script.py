from bs4 import BeautifulSoup
from selenium import webdriver
from unidecode import unidecode
from requests_html import HTMLSession


def get_page_data():
    url = 'https://wallex.ir/'
    with webdriver.Chrome() as driver:
        driver.get(url)
        source = driver.page_source

    return 'None'


def get_tether(session: HTMLSession):
    url = 'https://wallex.ir/'
    r = session.get(url)
    r.html.render(timeout=0, sleep=2)
    price = r.html.find('strong')
    return unidecode(price[5].text)
