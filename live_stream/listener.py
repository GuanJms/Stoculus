import asyncio
import json
import websockets

from abc import ABC, abstractmethod


class StreamListener(ABC):
    def __init__(self, uri):
        self.uri = uri
        self.local_port = None
        self.data_socket = None
        self.local_server = None

    async def connect_ws(self):
        async with websockets.connect(self.uri) as ws:
            self.data_socket = ws
            while True:
                response = await ws.recv()
                await self.process_response(response)
                # print(f"Received: {response}")

    async def handle_trigger(self, websocket, path, event):
        async for message in websocket:
            print(f"Trigger received: {message}")
            event.set()

    async def listener(self):
        event = asyncio.Event()
        trigger_server = websockets.serve(lambda ws, path: self.handle_trigger(ws, path, event), 'localhost',
                                          self.local_port)
        self.local_server = trigger_server

        async with trigger_server:
            while True:
                event.clear()
                ws_task = asyncio.create_task(self.connect_ws())
                event_task = asyncio.create_task(event.wait())
                await asyncio.wait(
                    [ws_task, event_task],
                    return_when=asyncio.FIRST_COMPLETED
                )
                if event.is_set():
                    ws_task.cancel()
                    print("Refreshing ws connection...")
                    try:
                        await ws_task
                    except asyncio.CancelledError:
                        pass

    @abstractmethod
    async def process_response(self, response):
        pass

    def run(self):
        asyncio.get_event_loop().run_until_complete(self.listener())
