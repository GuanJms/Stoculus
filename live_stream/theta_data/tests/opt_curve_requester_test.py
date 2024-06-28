from live_stream.theta_data.theta_requester import ThetaRequester
from middleware.requester import ThetaMetaRequester

r = ThetaRequester()

# Get all strikes for TSLA

requester = ThetaMetaRequester()
root = 'TSLA'
expiration = 20240628
strikes = requester.get_option_strikes(root, expiration)
print(strikes)
r.subscribe(sec_type='STOCK', req_type='TRADE', root=root, subscribe=True)
# r.subscribe(sec_type='STOCK', req_type='TRADE', root='SPY', subscribe=False)


for right in ['C', 'P']:
    for strike in strikes:
        r.subscribe(sec_type='OPTION', req_type='TRADE', root=root,
                    expiration=expiration, strike=strike, right=right, subscribe=True)

# for right in ['C']:
#     for strike in [170000, 18000]:
#         r.subscribe(sec_type='OPTION', req_type='QUOTE', root=root,
#                     expiration=expiration, strike=strike, right=right, subscribe=False)

