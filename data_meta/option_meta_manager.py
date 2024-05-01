from typing import List

from middleware.requester import ThetaMetaRequester
from path import PathManager
from ._meta_manager import MetaManager
from data_meta.meta_enums import MetaEnum
from _enums import DomainEnum, AssetDomain, EquityDomain
from .ticker_meta_manager import TickerMetaManager


class OptionMetaManager(MetaManager):

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'):
            cls.instance = super(OptionMetaManager, cls).__new__(cls)
        return cls.instance

    def __init__(self, **kwargs):
        super().__init__()
        self.meta = {}
        self.tickers = set()
        self.floor_date = kwargs.get('floor_date', None)
        self.ticker_manager = TickerMetaManager()
        self.requester = ThetaMetaRequester()
        self._verbose = kwargs.get('verbose', False)
        self.ticker_meta_path = {}
        self._cache = {}  # TODO: Add fixed memory cache which will drop the oldest data when it reaches the limit

    def load_meta(self, **kwargs):
        tickers = kwargs.get('tickers', [])
        if not tickers:
            self.tickers |= set(self.ticker_manager.get_meta())
            loaded_tickers = self.tickers
        else:
            loaded_tickers = set(tickers)  # type: set

        option_path = PathManager.get_meta_path([MetaEnum.OPTION])
        for ticker in loaded_tickers:
            ticker_json_file = ticker + '.json'
            ticker_path = option_path / ticker_json_file
            self.ticker_meta_path[ticker] = ticker_path
            try:
                self.meta[ticker] = self.read_json(ticker_path)
            except FileNotFoundError:
                print(f"Meta path not found for {ticker}")

    def get_option_meta(self, ticker: str):
        # load json file for ticker
        if ticker not in self.meta:
            self.load_meta(tickers=[ticker])
        if ticker not in self.meta:
            return None
        return self.meta[ticker]

    def get_option_expirations(self, ticker: str):
        option_meta_data = self.get_option_meta(ticker)
        if option_meta_data is None:
            return None
        exps_data = option_meta_data.get('all_expirations', None)
        return exps_data

    def update(self, **kwargs):
        self._verbose = kwargs.get('verbose', False)
        self.load_meta(**kwargs)
        # DONE: update all expirations
        for ticker in self.all_tickers:
            # DONE: Update available expirations for one ticker
            self._update_all_expirations(ticker)
            self.write_json_ticker(ticker)

        # TODO: update all expiration meta dates and strikes (if empty)
        for ticker in self.all_tickers:
            self._update_expirations_meta(ticker)
            self.write_json_ticker(ticker)

    def write_json_ticker(self, ticker: str):
        t_path = self.ticker_meta_path[ticker]
        self.overwrite_json(t_path, self.meta[ticker])

    def _update_all_expirations(self, ticker: str):
        if ticker not in self.meta:
            self.meta[ticker] = {}
        if 'all_expirations' not in self.meta[ticker]:
            self._update_root_expirations(ticker)

    def _update_expirations_meta(self, ticker: str):
        if 'exp_meta' not in self.meta[ticker]:
            self.meta[ticker]['exp_meta'] = {}
            # lack of one expiration meta
            # lack of strikes or dates
            # if 'strikes' not in self.meta[ticker]['exp_meta'][str(exp)]:
            #     self._update_exp_strike_meta(ticker, exp)
            # if 'dates' not in self.meta[ticker]['exp_meta'][str(exp)]:
            #     self._update_exp_date_meta(ticker, exp)

    def _update_root_expirations(self, ticker: str):
        """Update all available expirations for one ticker"""
        data = self.requester.get_option_expirations(ticker)
        if self.is_empty_data(data, f"Error getting expirations for {ticker}"):
            self.all_tickers.remove(ticker)
            return
        self.meta[ticker]['all_expirations'] = data
        if self._verbose:
            print(f"Updated {ticker} expirations - {data}")

    def _construct_exp_meta(self, ticker: str, exp: int):
        """Option expiration meta include available strikes and dates"""
        self.meta[ticker]['exp_meta'][str(exp)] = {}
        # self._update_exp_strike_meta(ticker, exp)
        # self._update_exp_date_meta(ticker, exp)

    def _update_exp_strike_meta(self, ticker: str, exp):
        data = self.requester.get_option_strikes(ticker, exp)
        if self.is_empty_data(data, f"Error getting strikes for {ticker} {exp}"): return
        self.meta[ticker]['exp_meta'][str(exp)]['strikes'] = data
        if self._verbose:
            print(f"Updated {ticker} {exp} strikes - {data}")

    def _update_exp_date_meta(self, ticker: str, exp):
        data = self.requester.get_option_exp_dates(ticker, exp)
        if self.is_empty_data(data, f"Error getting dates for {ticker} {exp}"): return
        self.meta[ticker]['exp_meta'][str(exp)]['dates'] = data
        if self._verbose:
            print(f"Updated {ticker} {exp} dates - {data}")

    @staticmethod
    def is_empty_data(data, empty_message):
        if data is None:
            print(empty_message)
            return True
        return False

    def update_exp_meta(self, ticker: str, exp: int, strikes: List[int]):
        if self.meta is None:
            self.load_meta(tickers=[ticker])
        if 'exp_meta' not in self.meta[ticker]:
            self.meta[ticker]['exp_meta'] = {}
        if exp not in self.meta[ticker]['exp_meta']:
            self._construct_exp_meta(ticker, exp)
        self.meta[ticker]['exp_meta'][str(exp)]['strikes'] = strikes
        self.write_json_ticker(ticker)

    def get_all_tickers(self) -> List[str]:
        return self.ticker_manager.get_meta()
