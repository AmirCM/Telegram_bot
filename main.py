import requests
from bs4 import BeautifulSoup
import json
from script import get_page_data


class Currency:
    def __init__(self):
        self.url = ['https://www.tgju.org/', 'https://web-api.coinmarketcap.com/v1/cryptocurrency/'
                                             'listings/latest?aux=circulating_supply,max_supply,total_'
                                             'supply&convert=USD&cryptocurrency_type=all&limit=100&sort=market'
                                             '_cap&sort_dir=desc&start=1']
        self.price = [0, 0, 0]
        self.crypto = {'Bitcoin': 'BTC',
                       'Ethereum': 'ETH',
                       'Monero': 'XMR',
                       'Dash': 'DASH',
                       'Litecoin': 'LTC',
                       'Tether': 'USDT',
                       'Cardano': 'ADA',
                       'TRON': 'TRX'}

        self.c_keys = ['price_dollar_rl', 'price_eur', 'price_gbp']

    def to_rial(self, c_prices):
        tether = get_page_data()
        print(tether)

        for k, v in c_prices.items():
            c_prices[k] = int(float(v) * tether)

        c_prices['USDT'] = int(tether)
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
        data = json.loads(r.text)
        data = data['data']
        c_price = {}
        for d in data:
            if d['name'] in self.crypto:
                c_price[self.crypto[d['name']]] = str(d['quote']['USD']['price'])

        # c_price['USDT'] = str(1 + round(float(c_price['USDT']) - int(float(c_price['USDT'])), 5) * 10)
        return c_price


if __name__ == '__main__':
    c = Currency()
    prices = c.update_db()
    rial = c.to_rial(prices.copy())
    rial['USDT'] = str(float(rial['USDT']) * 1.008)
    print(rial['USDT'])
