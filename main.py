import requests
from bs4 import BeautifulSoup

url = 'https://www.tgju.org/'

if __name__ == '__main__':
    r = requests.get(url)
    soup = BeautifulSoup(r.text, features='lxml')
    divs = soup.find_all('div', class_='home-fs-row')
    d_in_d = []
    for d in divs:
        d_in_d += d.find_all('table', class_='data-table market-table dark-head market-section-right')

    tables_header = d_in_d[0].find_all('th')
    for i, t in enumerate(tables_header):
        if t.text == "دلار":
            print('Dollar', i)
        elif t.text == "یورو":
            print('EURO', i)
        elif t.text == "پوند انگلیس":
            print('POND', i)


