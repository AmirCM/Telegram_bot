import requests
from bs4 import BeautifulSoup
import json

url = 'https://web-api.coinmarketcap.com/v1/cryptocurrency/listings/latest?aux=circulating_supply,max_supply,total_supply&convert=USD&cryptocurrency_type=all&limit=100&sort=market_cap&sort_dir=desc&start=1'
r = requests.get(url)
data = json.loads(r.text)
cpy = data['data']
for i, l in enumerate(cpy):
    print(i, l['name'], l['quote']['USD']['price'])
