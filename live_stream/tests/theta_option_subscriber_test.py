from live_stream.theta_data.theta_requester import ThetaRequester

subs = ThetaRequester()
subs.subscribe(req_type='TRADE', root='NVDA', strike=950000, right='C', expiration='20240524')
