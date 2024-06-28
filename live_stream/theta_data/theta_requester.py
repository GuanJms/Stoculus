import asyncio

from live_stream.requester import StreamRequester
from live_stream.theta_data.request_maker import RequestMaker


class ThetaRequester(StreamRequester):

    def __init__(self):
        super().__init__()
        self.data_uri['OPTION'] = "ws://127.0.0.1:25520/v1/events"
        self.data_uri['STOCK'] = "ws://127.0.0.1:25521/v1/events"
        self.add_local_server(port=7777, sec_type='OPTION')
        self.add_local_server(port=7778, sec_type='STOCK')

    def subscribe(self, sec_type, **kwargs):
        try:
            match sec_type:
                case "OPTION":
                    req = RequestMaker.create_option_request(**kwargs)
                    self._send_request(req, sec_type=sec_type)
                    print("Option request sent")

                case "STOCK":
                    req = RequestMaker.create_stock_request(**kwargs)
                    self._send_request(req, sec_type=sec_type)
                case _:
                    raise ValueError(f"sec_type must be one of ['OPTION', 'STOCK']")
        except Exception as e:
            print(f"An error occurred: {e}")

        # send status update to local server
        try:
            asyncio.get_event_loop().run_until_complete(self.send_local("Status update: Request sent", sec_type))
        except Exception as e:
            print(f"An error occurred: {e}")

    def unsubscribe_all(self):
        req = RequestMaker.create_unsubscribe_all_request()
        self._send_request(req, sec_type='OPTION')
        self._send_request(req, sec_type='STOCK')

    def refresh_all(self):
        for sec_type in ['OPTION', 'STOCK']:
            try:
                asyncio.get_event_loop().run_until_complete(self.send_local("Status update: Request sent", sec_type))
            except Exception as e:
                print(f"An error occurred: {e}")

#
# r = ThetaRequester()
# subscribe = False
#
# r.subscribe('OPTION', req_type='QUOTE', root='NVDA', expiration=20240524, strike=950000, right='C', subscribe=subscribe)
# r.subscribe('OPTION', req_type='QUOTE', root='NVDA', expiration=20240524, strike=960000, right='C', subscribe=subscribe)
# r.subscribe('OPTION', req_type='QUOTE', root='NVDA', expiration=20240524, strike=970000, right='C', subscribe=subscribe)
# # # run tasks
# r.subscribe(sec_type='STOCK', req_type='QUOTE', root='NVDA', subscribe=subscribe)
