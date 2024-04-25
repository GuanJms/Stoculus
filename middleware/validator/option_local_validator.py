from typing import List, Dict

from ._local_validator import LocalValidator
from _enums import AssetDomain, EquityDomain, PriceDomain
import json


class OptionLocalValidator(LocalValidator):

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'):
            cls.instance = super(OptionLocalValidator, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        super().__init__()
        self._domain = [AssetDomain.EQUITY, EquityDomain.OPTION]

    def check_valid_ticker(self, ticker: str):
        try:
            self._check_existence(sub_path=[ticker])
        except (FileNotFoundError, ValueError):
            return False
        return True

    def load_meta_file(self, ticker: str) -> dict:
        if not self._check_existence(sub_path=[ticker, 'meta.json']):
            raise FileNotFoundError(f"meta file not found for {ticker}")
        path = self.get_director_path() / ticker / 'meta.json'
        with open(path, 'r') as file:
            meta_data = json.load(file)
        return meta_data

    def _get_exps(self, ticker: str) -> List[int]:
        meta_data = self.load_meta_file(ticker)
        try:
            exps = meta_data.get('EXPIRATIONS')
            return exps
        except Exception as e:
            raise ValueError(f"meta file does not contain expirations: {e}")

    def _get_exps_strikes(self, ticker: str) -> Dict[int, List[int]]:
        meta_data = self.load_meta_file(ticker)
        try:
            exps_strikes = meta_data.get('STRIKES')
            return exps_strikes
        except Exception as e:
            raise ValueError(f"meta file does not contain expirations and strikes: {e}")

    def _get_strikes(self, ticker: str, exp: int) -> List[int]:
        exps_strikes = self._get_exps_strikes(ticker)
        try:
            strikes = exps_strikes.get(exp)
            return strikes
        except Exception as e:
            raise ValueError(f"meta file does not contain strikes for expiration {exp}: {e}")
