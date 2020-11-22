import time
from selenium import webdriver
from unidecode import unidecode
from requests_html import HTMLSession
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException


def get_page_data():
    url = 'https://wallex.ir/'
    driver = webdriver.PhantomJS()

    #executor_url = driver.command_executor._url
    #session_id = driver.session_id

    #print(session_id)
    #print(executor_url)

    driver.get(url)
    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')
    prices = soup.find_all('strong')

    return unidecode(prices[5].text)

