from live_stream.theta_data.theta_requester import ThetaRequester

r = ThetaRequester()
#

for strike in ['175000', '180000', '177500']:
    r.subscribe(sec_type='OPTION', req_type='TRADE', root='TSLA',
                expiration='20240524', strike=strike, right='C', subscribe=True)

# r.subscribe(sec_type='OPTION', req_type='QUOTE', root='NVDA',
#             expiration='20240524', strike='1000000', right='C', subscribe=True)

# r.subscribe(sec_type='STOCK', req_type='TRADE', root='NVDA', subscribe=False)

r.unsubscribe_all()

# Received: {"header":{"type":"TRADE","status":"CONNECTED"},
# "contract":{"security_type":"OPTION","root":"NVDA",
# "expiration":20240524,"strike":950000,"right":"C"},"t
# rade":{"ms_of_day":48950202,"sequence":-600833752,"si
# ze":2,"condition":18,"price":44.3,"exchange":69,"date":20240516}}
