import requests
from bs4 import BeautifulSoup
import re


class Currency:
    def __init__(self):
        self.url = ['https://www.tgju.org/', 'https://coinmarketcap.com/']
        self.price = [0, 0, 0]
        self.crypto = {'BTC': r'^Bitcoin\d{1,2}BTC$',
                       'ETH': r'^Ethereum\d{1,2}ETH$',
                       'XMR': r'^Monero\d{1,2}XMR$',
                       'DASH': r'^Dash30DASH$',
                       'LTC': r'^Litecoin\d{1,2}LTC$',
                       'USDT': r'^Tether\d{1,2}USDT$',
                       'ADA': r'^Cardano\d{1,2}ADA$',
                       'TRX': r'^TRON\d{1,2}TRX$'}

        self.c_keys = ['price_dollar_rl', 'price_eur', 'price_gbp']

    def to_rial(self, c_prices):
        for k, v in c_prices.items():
            v = v.split('$')[1].split(',')
            if len(v) > 1:
                v = v[0] + v[1]
            else:
                v = v[0]
            c_prices[k] = int(float(v) * self.price[0])
        return c_prices

    def update_db(self):
        r = requests.get(self.url[0])
        soup = BeautifulSoup(r.text, features='lxml')
        divs = soup.find_all('div', class_='home-fs-row')
        d_in_d = []
        for d in divs:
            d_in_d += d.find_all('table', class_='data-table market-table dark-head market-section-right')
        d_in_d = d_in_d[0]

        for i in range(3):
            price = d_in_d.find('tr', {"data-market-row": self.c_keys[i]}).find('td', {'class': 'nf'}).text.split(
                ',')
            self.price[i] = int(price[0]) * 100 + int(price[1]) // 10

        r = requests.get(self.url[1])
        soup = BeautifulSoup(r.text, features='lxml')
        table = soup.find('table', class_='cmc-table cmc-table___11lFC cmc-table-homepage___2_guh')
        key = False
        c_price = {}

        for i, a in enumerate(table.find_all('a')):
            if i % 4 == 0:
                for cryp, val in self.crypto.items():
                    if re.match(val, a.text):
                        key = cryp
                        break
            elif i % 4 == 1 and key:
                c_price[key] = a.text
                key = False

        return c_price


if __name__ == '__main__':
    c = Currency()
    pr = c.update_db()
    print(c.to_rial(pr.copy()))
    print(pr)
