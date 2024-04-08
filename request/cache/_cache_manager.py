from typing import List, TYPE_CHECKING

from _enums import ReadingStatus

if TYPE_CHECKING:
    from reader import StreamReader
from request.cache.cache_basics._data_cache import DataCache


class CacheManager:
    _data_caches: dict[str, DataCache] = {}  # token: DataCache
    _readers: dict[str, List['StreamReader']] = {}  # token: Reader

    @classmethod
    def create_cache(cls, token: str):
        cls._data_caches[token] = DataCache(token)

    @classmethod
    def get_cache(cls, token: str) -> DataCache:
        return cls._data_caches.get(token, None)

    @classmethod
    def get_readers(cls, token) -> list['StreamReader']:
        return cls._readers.get(token, [])

    @classmethod
    def register_reader(cls, token: str, reader: 'StreamReader'):
        reader.set_data_cache(cls.get_cache(token))
        cls._readers.setdefault(token, []).append(reader)

    @classmethod
    def _is_reading_request_finished(cls, token: str) -> bool:
        return all(reader.reading_status == ReadingStatus.DONE for reader in cls.get_readers(token))

    @classmethod
    def update_cache_status(cls, token):
        if cls._is_reading_request_finished(token):
            cls.get_cache(token).set_status(ReadingStatus.DONE)
        else:
            cls.get_cache(token).set_status(ReadingStatus.ONGOING)
