import requests
from bs4 import BeautifulSoup

url = 'https://www.tgju.org/'


class Currency:
    def __init__(self, table):
        self.table = table
        price = self.table.find('td', {'class': 'nf'}).text
        price = price.split(',')
        self.price = int(price[0])*100 + int(price[1])//10


if __name__ == '__main__':
    r = requests.get(url)
    soup = BeautifulSoup(r.text, features='lxml')

    divs = soup.find_all('div', class_='home-fs-row')
    d_in_d = []
    for d in divs:
        d_in_d += d.find_all('table', class_='data-table market-table dark-head market-section-right')
    d_in_d = d_in_d[0]

    dollar = Currency(d_in_d.find('tr', {"data-market-row": "price_dollar_rl"}))
    eur = Currency(d_in_d.find('tr', {"data-market-row": "price_eur"}))
    gbp = Currency(d_in_d.find('tr', {"data-market-row": "price_gbp"}))

    print(dollar.price, eur.price, gbp.price)
