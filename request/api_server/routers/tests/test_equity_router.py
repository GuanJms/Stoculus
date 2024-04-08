import unittest

import requests


class MyEquityRouterTest(unittest.TestCase):
    def test_get_quote(self):
        port = '8000'
        base_url = 'http://127.0.0.1'
        url = f'{base_url}:{port}/equity/stock/quote'
        ticker = 'AAPL'
        quote_date = 10100
        response = requests.get(url, params={'ticker': ticker, 'date': quote_date})
        print(response.status_code)
        print(response.json())


if __name__ == '__main__':
    unittest.main()
