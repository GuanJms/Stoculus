from abc import ABC, abstractmethod


class BaseHandler(ABC):

    @abstractmethod
    async def process(self, response):
        pass
