import asyncio
import websockets
from live_stream.listener import StreamListener
from live_stream.response_handlers.format_handler import FormatHandler
from live_stream.response_handlers.kafka_handler import KafkaHandler


class ThetaStockStreamListener(StreamListener):

    def __init__(self):
        uri = "ws://127.0.0.1:25521/v1/events"
        super().__init__(uri)
        self.local_port = 7778
        self.kafka_handler = KafkaHandler()
        self.format_handler = FormatHandler()

    async def process_response(self, response):
        if 'contract' not in response:
            return
        response = await self.format_handler.process(response)
        await self.kafka_handler.process(response)

        # Received: {"header": {"type": "QUOTE", "status": "CONNECTED"},
        #            "contract": {"security_type": "STOCK", "root": "NVDA"},
        #            "quote": {"ms_of_day": 39626150, "bid_size": 7, "bid_exchange": 29, "bid": 947.27,
        #                      "bid_condition": 0, "ask_size": 233, "ask_exchange": 29, "ask": 947.51, "ask_condition": 0,
        #                      "date": 20240521}}
#
# Received: {"header":{"type":"QUOTE","status":"CONNECTED"},"contract":{"security_type":"STOCK","root":"NVDA"},
# "quote":{"ms_of_day":39655484,"bid_size":50,"bid_exchange":29,"bid":947.3,"bid_condition":0,"ask_size":6,"ask_exchange":29,"ask":947.44,"ask_condition":0,"date":20240521}}

# Received: {"header":{"type":"OHLC","status":"CONNECTED"},"contract":{"security_type":"STOCK","root":"NVDA"},
# "ohlc":{"ms_of_day":39657065,"open":953.85,"high":956.6,"low":931.55,"close":947.51,"volume":10046138,"count":244304,"date":20240521}}

# Received: {"header":{"type":"TRADE","status":"CONNECTED"},"contract":{"security_type":"STOCK","root":"NVDA"},
# "trade":{"ms_of_day":39657065,"sequence":11529168,"size":1,"condition":115,"price":947.51,"exchange":57,"date":20240521}}


#
# test = ThetaStockStreamListener()
# test.run()
