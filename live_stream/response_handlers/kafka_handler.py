from kafka import KafkaProducer
import json as json

from live_stream.response_handlers.base_handler import BaseHandler


def serializer(message):
    return json.dumps(message).encode('utf-8')


class KafkaHandler(BaseHandler):
    def __init__(self, port=9092):
        super().__init__()
        self.port = port
        self.producer = KafkaProducer(
            bootstrap_servers=[f'localhost:{port}'],
            value_serializer=serializer
        )

    async def process(self, response):
        if response is None or response == 'None':
            return
        if 'contract' not in response:
            return
        flat_record = json.dumps(response)
        topic = self.get_topic(response)
        self.producer.send(topic, flat_record)
        self.producer.flush()

    def get_topic(self, response):
        root = response['contract']['root']
        date = response['data']['date']
        return f'{root}_stream_{date}'

