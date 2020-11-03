import requests
from bs4 import BeautifulSoup


class Currency:
    def __init__(self):
        self.url = ['https://www.tgju.org/', 'https://coinmarketcap.com/']
        self.price = [0, 0, 0]
        self.crypto = {'BTC': 'Bitcoin1BTC', 'ETH': 'Ethereum2ETH',
                       'XMR': 'Monero14XMR', 'DASH': 'Dash30DASH', 'LTC': 'Litecoin8LTC', 'USDT': 'Tether3USDT',
                       'ADA': 'Cardano11ADA', 'TRX': 'TRON15TRX'}

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
        prices = ['Bitcoin1BTC', 'Ethereum2ETH',
                  'TRON15TRX', 'Dash30DASH', 'Litecoin8LTC', 'Cardano11ADA',
                  'Monero14XMR', 'Tether3USDT']
        key = False
        c_price = {}
        for i, a in enumerate(table.find_all('a')):
            if i % 4 == 0 and a.text in prices:
                key = a.text
            elif i % 4 == 1 and key:
                for k, v in self.crypto.items():
                    if v == key:
                        c_price[k] = a.text
                key = False

        return c_price


if __name__ == '__main__':
    c = Currency()
    pr = c.update_db()
    print(c.to_rial(pr.copy()))
    print(pr)
