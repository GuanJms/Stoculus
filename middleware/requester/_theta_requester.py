import requests


class ThetaRequester:
    url = 'http://127.0.0.1:25510/v2'

    @staticmethod
    def parse_response(response):
        status_code = response.status_code
        if status_code != 200:
            print(f"Error: {status_code}")
            return None
        return response.json().get('response', None)

    @staticmethod
    def get_request(url, params=None):
        response = requests.get(url, params=params)
        return ThetaRequester.parse_response(response)
