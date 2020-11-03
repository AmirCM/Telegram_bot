from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json

api_token = 'd6d46302-3592-455d-ac29-2d60b0787950'
url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
parameters = {
    'start': '1',
    'limit': '1',
    'convert': 'USD'
}
headers = {
    'Accepts': 'application/json',
    'X-CMC_PRO_API_KEY': 'd6d46302-3592-455d-ac29-2d60b0787950',
}

session = Session()
session.headers.update(headers)

try:
    response = session.get(url, params=parameters)
    data = json.loads(response.text)
    print(data['data'][0]['quote']['USD']['price'])
except (ConnectionError, Timeout, TooManyRedirects) as e:
    print('err', e)
