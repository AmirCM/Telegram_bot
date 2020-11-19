from bs4 import BeautifulSoup
from selenium import webdriver
from unidecode import unidecode
from requests_html import HTMLSession


def get_page_data():


    """
    with webdriver.Chrome() as driver:
        driver.get(url)
        source = driver.page_source
        """

    return 'None'


def get_tether():
    url = 'https://wallex.ir/'

    session = HTMLSession()
    r = session.get(url)
    r.html.render()
    price = r.html.find('strong')
    return unidecode(price[5].text)


print(get_tether())
