from typing import List, Dict

from ._local_validator import LocalValidator
from _enums import AssetDomain, EquityDomain, PriceDomain
import json


class OptionLocalValidator(LocalValidator):

    def __init__(self):
        super().__init__()
        self._domain = [AssetDomain.EQUITY, EquityDomain.OPTION]
        self._cache = {}

    @staticmethod
    def check_valid_ticker(ticker: str):
        from data_meta.ticker_meta_manager import TickerMetaManager
        manager = TickerMetaManager()
        return manager.has_ticker(ticker)

    def get_option_meta(self, ticker: str) -> dict:
        from data_meta.option_meta_manager import OptionMetaManager
        manager = OptionMetaManager()
        if ticker not in self._cache:
            self._cache[ticker] = manager.get_option_meta(ticker)
        return self._cache[ticker]

    def get_exps(self, ticker: str) -> List[int] | None:
        meta_data = self.get_option_meta(ticker)
        if meta_data is None: return None
        return meta_data.get('all_expirations', None)

    def get_strikes(self, ticker: str, exp: int) -> List[int] | None:
        if not self._has_option_chain_meta(ticker, exp): return None
        meta_data = self.get_option_meta(ticker)
        _option_chain_meta = meta_data.get(exp)
        return _option_chain_meta.get('strikes', None)

    def get_dates(self, ticker: str, exp: int) -> List[str] | None:
        if not self._has_option_chain_meta(ticker, exp): return None
        meta_data = self.get_option_meta(ticker)
        _option_chain_meta = meta_data.get(exp)
        return _option_chain_meta.get('dates', None)

    def _has_option_chain_meta(self, ticker: str, exp: int) -> bool:
        meta_data = self.get_option_meta(ticker)
        if meta_data is None: return False
        exp_meta = meta_data.get('exp_meta')
        return exp in exp_meta
