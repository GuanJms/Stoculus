import asyncio
import json

import websockets
from abc import ABC, abstractmethod


class StreamRequester(ABC):
    def __init__(self):
        self.data_uri = {}
        self.local_port = {}
        self.local_sever_uri = {}

    def add_local_server(self, port, sec_type):
        if sec_type not in ['OPTION', 'STOCK']:
            raise ValueError(f"sec_type must be one of ['OPTION', 'STOCK']")
        self.local_port[sec_type] = port
        self.local_sever_uri[sec_type] = f'ws://localhost:{port}'

    async def send(self, data, sec_type):
        self._check_sec_type(sec_type)
        uri = self.data_uri[sec_type]
        async with websockets.connect(uri) as websocket:
            json_str = json.dumps(data)
            print(f"Sending: {json_str} to {uri}")
            await websocket.send(json_str)

    async def send_local(self, data, sec_type):
        self._check_sec_type(sec_type)
        local_sever_uri = self.local_sever_uri[sec_type]
        async with websockets.connect(local_sever_uri) as local_server:
            json_str = json.dumps(data)
            print(f"Sending: {json_str} to {local_sever_uri}")
            await local_server.send(json_str)

    def _send_request(self, req, sec_type):
        asyncio.get_event_loop().run_until_complete(self.send(req, sec_type))

    @abstractmethod
    async def subscribe(self, sec_type, **kwargs):
        pass

    def _check_sec_type(self, sec_type):
        if sec_type not in ['OPTION', 'STOCK']:
            raise ValueError(f"sec_type must be one of ['OPTION', 'STOCK']")
        if self.local_port[sec_type] is None or self.local_sever_uri[sec_type] is None:
            raise ValueError(f"Local server for {sec_type} not found")

