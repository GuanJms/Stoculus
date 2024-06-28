from live_stream.response_handlers.base_handler import BaseHandler
import asyncio
import websockets


#  this is the handler for transmitting the data to the client

class TCPHandler(BaseHandler):
    def __init__(self, port):
        super().__init__()
        self.port = port

    async def process(self, response):
        try:
            async with websockets.connect(f"ws://localhost:{self.port}") as ws:
                print(f"Sending response: {response}")
                await ws.send(response)
        except Exception as e:
            print(f"An error occurred: {e}")
