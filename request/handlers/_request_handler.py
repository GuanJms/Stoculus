from reader import ReaderFactory
from request.handlers.tokens import TokenManager
from request.cache import CacheManager


class RequestHandler:

    @staticmethod
    def create_timeline_cache():
        encrypted_token, key, original_token = TokenManager.generate_token()
        CacheManager.create_cache(original_token)
        return encrypted_token, key, original_token

    @staticmethod
    def handle_read_upto_time_request(token: str, time: int | float):
        # Readers read more data into cache
        readers = CacheManager.get_readers(token)
        for reader in readers:
            reader.read(time=time, return_type='json', push_to_cash=True)
        CacheManager.update_cache_status(token)
        data_cache = CacheManager.get_cache(token)
        data = data_cache.read()
        read_status = data_cache.status

        return {
            'data': data,
            'status': read_status.name
        }

    @staticmethod
    def create_reader(domain_chain_str, token, **kwargs):
        reader = ReaderFactory.create_reader(domain_chain_str=domain_chain_str, **kwargs)
        try:
            reader.configure_file()
            reader.open_stream()
            CacheManager.register_reader(token, reader)
        except FileNotFoundError as e:
            raise ValueError(str(e))




    @staticmethod
    def get_cache_status(token):
        cache = CacheManager.get_cache(token)
        if cache is None:
            return 'INVALID TOKEN'
        return CacheManager.get_cache(token).status.name

    @staticmethod
    def find_token(hub_id: str):
        token = CacheManager.find_token(hub_id)
        return token

    @classmethod
    def delete_token(cls, token: str):
        CacheManager.delete_token(token)

    @classmethod
    def register_token(cls, hub_id: str, token: str):
        CacheManager.register_token(hub_id, token)

    @classmethod
    def get_tickers(cls, token):
        return CacheManager.get_tickers(token)

    @classmethod
    def get_server_status(cls):
        return CacheManager.get_cache_manager_status()




