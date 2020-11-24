from unidecode import unidecode
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


"""
def get_page_data2():
    url = 'https://wallex.ir/'
    driver.get(url)
    driver.execute_script('window.scrollTo(0, document.body.scrollHeight)')
    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')
    prices = soup.find_all('strong')

    return unidecode(prices[5].text)
"""

def get_page_data():
    data = {
        "srcCurrency": "usdt", "dstCurrency": "rls"
    }
    r = requests.post('https://api.nobitex.ir/market/stats', data=data)
    tether = int(float(r.json()['stats']['usdt-rls']['latest']) // 10)
    return tether


