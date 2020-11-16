from bs4 import BeautifulSoup
from selenium import webdriver
from unidecode import unidecode


def get_page_data():
    url = 'https://wallex.ir/'
    with webdriver.Chrome() as driver:
        driver.get(url)
        source = driver.page_source
    return source


def get_tether():
    source = get_page_data()
    soup = BeautifulSoup(source, features='lxml')
    price = soup.findAll('strong')
    return unidecode(price[5].text)


