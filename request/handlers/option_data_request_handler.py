from typing import List

import pandas as pd

from configuration import ConfigurationManager
from path import PathManager
from utils._domain_operations import parse_domain
from utils._json_operations import read_json_file_to_dict

import json


class OptionDataRequestHandler:
    _cache = {}

    @classmethod
    def get_option_chain_historical_quote(cls, ticker: str, exp: int, year: int, month: int):
        if not cls._is_valid(ticker=ticker, exp=exp):
            return None
        try:
            path = PathManager.get_path(domains=parse_domain("EQUITY.OPTION.EOD"), root=ticker, exp=exp, year=year,
                                        month=month, file_type='csv')
            data = pd.read_csv(path)  # TODO: modify to get rid of pandas for converting to dict
            data.fillna(-999, inplace=True)
            data = data.to_dict()
            return data
        except FileNotFoundError:
            return None

    @classmethod
    def get_option_expiration_dates(cls, ticker: str):
        # TODO: use option meta manager to get expiration dates
        from data_meta import OptionMetaManager
        manager = OptionMetaManager()
        return manager.get_option_expirations(ticker)

    @classmethod
    def _is_valid(cls, **kwargs) -> bool:
        keys = set(kwargs.keys())
        if keys == {'ticker'}:
            return cls._is_valid_ticker(ticker=kwargs['ticker'])
        elif keys == {'ticker', 'exp'}:
            return cls._is_valid_option_chain(ticker=kwargs['ticker'], exp=kwargs['exp'])
        else:
            return False

    @classmethod
    def _is_valid_ticker(cls, ticker: str) -> bool:
        # TODO: Add admin API request to refresh the cache daily or weekly
        if cls._cache.get('tickers', None) is None:
            tickers = cls.get_available_option_tickers()
            cls._cache['tickers'] = tickers
        if ticker in cls._cache['tickers']:
            return True
        else:
            return False

    @classmethod
    def _is_valid_option_chain(cls, ticker: str, exp: int) -> bool:
        if not cls._is_valid_ticker(ticker):
            return False
        from data_meta import OptionMetaManager
        manager = OptionMetaManager()
        exps = manager.get_option_expirations(ticker)
        if exp in exps:
            return True
        else:
            return False

    @classmethod
    def get_option_expiration_strikes(cls, ticker: str, exp: int) -> List[int] | None:
        if not cls._is_valid(ticker=ticker, exp=exp):
            return None
        from middleware.pipeline import ValidationPipeline
        pipeline = ValidationPipeline()
        data = pipeline.get_strikes(ticker=ticker, exp=exp)
        if data is [] or data is None:
            return None
        return data

    @classmethod
    def get_available_option_tickers(cls):
        """ This function returns the list of available option tickers in Stoculus """
        from data_meta import OptionMetaManager
        manager = OptionMetaManager()
        tickers = manager.get_all_tickers()
        return tickers

# OptionDataRequestHandler.get_option_chain_historical_quote('SPY', 20240417)
