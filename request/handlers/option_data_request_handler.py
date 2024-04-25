import pandas as pd

from configuration import ConfigurationManager
from path import PathManager
from utils._domain_operations import parse_domain
from utils._json_operations import read_json_file_to_dict

import json


class OptionDataRequestHandler:
    expiration_dates = read_json_file_to_dict("D:\TempDataHouse\Logs\expiration.json")  # TODO: remove hard coded path

    @classmethod
    def get_option_chain_historical_quote(cls, ticker: str, exp: int, year: int, month: int):
        if ticker not in cls.expiration_dates and exp not in cls.expiration_dates[ticker]:
            return None
        try:
            path = PathManager.get_path(domains=parse_domain("EQUITY.OPTION.EOD"), root=ticker, exp=exp, year=year,
                                        month=month, file_type='csv')
            data = pd.read_csv(path)
            data.fillna(-99, inplace=True)
            data = data.to_dict()
            return data
        except FileNotFoundError:
            return None

    @classmethod
    def get_option_expiration_dates(cls, ticker: str):
        if ticker in cls.expiration_dates:
            return cls.expiration_dates[ticker]
        else:
            raise ValueError(f"Ticker {ticker} not found in expiration dates")

    @classmethod
    def check_ticker_existence_local(cls, ticker: str):
        """ This function checks if the ticker is in the expiration dates """
        if ticker in cls.expiration_dates:
            return True
        else:
            return False


    # @classmethod
    # def check_ticker_existence_theta_data_api(cls, ticker: str):
    #     # Check if the theta data api has the ticker


# OptionDataRequestHandler.get_option_chain_historical_quote('SPY', 20240417)
