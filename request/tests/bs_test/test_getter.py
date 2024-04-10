from urllib import request, parse
import json
import colorama

from unittest import TestCase
import requests

BASE = r'http://127.0.0.1:1999'


def read_next_line(time, public_token, private_key):
    url = f'{BASE}/timeline/time/next/'
    response = requests.get(url, params={'public_token': public_token, 'key': private_key, 'time': time})
    if response.status_code == 200:
        return response.json()
    else:
        print("Error:", response.status_code)


def start_connection(ticker='TSLA', date='20240301'):
    url = f'{BASE}/timeline/start/'
    ticker_info = {
        ticker: {
            'DOMAINS': 'EQUITY.STOCK.QUOTE',
            'DATE': date
        }
    }
    data = json.dumps(ticker_info).encode('utf-8')
    params = {'hub_id': '1234567899'}
    if params:
        query_string = parse.urlencode(params)
        url = f"{url}?{query_string}"
    req = request.Request(url, data=data, headers={'Content-Type': 'application/json'}, method='POST')
    with request.urlopen(req) as response:
        response_data = response.read()
        data = json.loads(response_data)
        return data


class TestRequestDataServer(TestCase):

    def setUp(self):
        connection_data_json = start_connection()
        self.public_token = connection_data_json['public_token']
        self.private_key = connection_data_json['private_key']
        self.failed_tickers = connection_data_json['failed_tickers']
        self.errors = connection_data_json['errors']
        print("public_token:", self.public_token, type(self.public_token))
        print("private_key:", self.private_key, type(self.private_key))
        print("failed_tickers:", self.failed_tickers)
        print("errors:", self.errors)

    def test_request_timeline_status(self):
        url = f'{BASE}/timeline/status/'
        response = requests.get(url, params={'public_token': self.public_token, 'key': self.private_key})

        # Check the response
        if response.status_code == 200:
            print("Success:", response.json())
        else:
            print("Error:", response.status_code)

    def test_read_next_time(self):
        from pprint import pprint
        received_data = []
        time = 45650000
        received_data = []
        data = read_next_line(time, self.public_token, self.private_key)
        received_data.append(data['data'])
        while data['status'] != 'DONE':
            data = read_next_line(time, self.public_token, self.private_key)
            received_data.append(data['data'])

        print("Length of received data:", len(received_data))
        print("Length of each data:", len(received_data[0]))
        print("Key of each data:", received_data[0][0].keys())
        print("Data: ", len(received_data[0][0]['data']))
        print("ticker:, ", received_data[0][0]['ticker'])
        print("domains:, ", received_data[0][0]['domains'])
        print("date:, ", received_data[0][0]['date'])
        print("headers:, ", received_data[0][0]['header'])



