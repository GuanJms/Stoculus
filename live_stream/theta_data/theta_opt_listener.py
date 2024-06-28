import asyncio
import websockets
from live_stream.listener import StreamListener
from live_stream.response_handlers import TCPHandler
from live_stream.response_handlers.format_handler import FormatHandler
from live_stream.response_handlers.kafka_handler import KafkaHandler


class ThetaOptionStreamListener(StreamListener):

    def __init__(self):
        uri = "ws://127.0.0.1:25520/v1/events"
        super().__init__(uri)
        self.local_port = 7777
        self.tcp_handler = TCPHandler(1777)
        self.kafka_handler = KafkaHandler()
        self.format_handler = FormatHandler()

    async def process_response(self, response):
        if 'contract' not in response:
            return
        response = await self.format_handler.process(response)
        await self.kafka_handler.process(response)

#
# test = ThetaOptionStreamListener()
# test.run()
