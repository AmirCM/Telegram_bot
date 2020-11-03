import requests
from bs4 import BeautifulSoup


class Currency:
    def __init__(self):
        self.url = ['https://www.tgju.org/', 'https://coinmarketcap.com/']
        self.price = [0, 0, 0]
        self.crypto = ['Bitcoin1BTC', 'Ethereum2ETH', 'TRON15TRX', 'Dash29DASH', 'Litecoin8LTC', 'Cardano11ADA',
                       'Monero14XMR', 'Tether3USDT']
        self.c_keys = ['price_dollar_rl', 'price_eur', 'price_gbp']

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
        prices = {}
        for i, a in enumerate(table.find_all('a')):
            if i % 4 == 0:
                key = a.text
            elif i % 4 == 1:
                prices[key] = a.text

        for p in prices:
            print(p)
        print(len(prices))


if __name__ == '__main__':
    c = Currency()
    c.update_db()
    print(c.price)
