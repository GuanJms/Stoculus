from reader import ReaderFactory
from request.handlers.tokens import TokenManager
from request.cache import CacheManager
import pandas as pd


class FundamentalDataRequestHandler:


    @staticmethod
    def get_financial_ratio(ticker: str):
        # TODO: create a data fetcer for financial ratio
        try:
            data = pd.read_csv(rf'D:\TempDataHouse\financial_ratios\{ticker}.csv')
            data.fillna(-99, inplace=True)
            data = data.to_dict(orient='records')
            return data
        except FileNotFoundError:
            return None