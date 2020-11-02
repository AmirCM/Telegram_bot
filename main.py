import requests
from bs4 import BeautifulSoup

dollar = 0
eur = 1
gbp = 2


class Currency:
    def __init__(self):

        self.url = ['https://www.tgju.org/']
        self.soup = [None, None, None]
        self.price = [0, 0, 0]
        self.c_keys = ['price_dollar_rl', 'price_eur', 'price_gbp']

    def update_db(self):
        r = requests.get(self.url[0])
        self.soup[0] = BeautifulSoup(r.text, features='lxml')
        divs = self.soup[0].find_all('div', class_='home-fs-row')
        d_in_d = []
        for d in divs:
            d_in_d += d.find_all('table', class_='data-table market-table dark-head market-section-right')
        d_in_d = d_in_d[0]

        for i in range(3):
            price = d_in_d.find('tr', {"data-market-row": self.c_keys[i]}).find('td', {'class': 'nf'}).text.split(
                ',')
            self.price[i] = int(price[0]) * 100 + int(price[1]) // 10


if __name__ == '__main__':
    c = Currency()
    c.update_db()
    print(c.price)
