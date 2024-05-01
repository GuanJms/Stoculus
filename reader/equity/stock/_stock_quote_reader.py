from pathlib import Path
from typing import List, Optional, Tuple
from ..._time_data_reader import TimeDataStreamReader
from _enums import AssetDomain, EquityDomain, PriceDomain, ReadingStatus

from configuration import ConfigurationManager
from utils._domain_operations import domain_to_chains


# TODO: Add metaclass if there is need to automate update Path process

class StockQuoteReader(TimeDataStreamReader):

    def __init__(self, **kwargs):
        super().__init__()
        self._domains = [AssetDomain.EQUITY, EquityDomain.STOCK, PriceDomain.QUOTE]
        self._root = kwargs.get('root')
        self._date = kwargs.get('date')

    @property
    def root(self) -> str:
        return self._root

    def set_root(self, root: str):
        self._root = root

    def configure_file(self):
        from path import PathManager
        # Setting file reading type
        domain_config = ConfigurationManager.get_domain_config(domains=self._domains)  # type: dict
        self._file_type = domain_config.get("FILE_TYPE", None)
        self._intraday_time_column = domain_config.get("TIME_COLUMN", None)
        self._encoding = domain_config.get("ENCODING", 'utf-8')
        self._delimiter = domain_config.get("DELIMITER", ',')
        if domain_config['HAS_HEADER'] is not None:
            self._has_header = True if domain_config['HAS_HEADER'] == 'True' else False

        # Setting Path
        new_path = PathManager.get_path(domains=self._domains, root=self._root,
                                            date=self._date, file_type=self._file_type)
        self.set_path(new_path)



    def jsonfy(self, data: List[List], time: int):
        return {
            "date": self._date,
            "root": self._root,
            "domains": "EQUITY.STOCK.QUOTE",
            "time": time,
            "data": data,
            "header": self._header,
        }

    def tag(self, data: List[List], **kwargs):
        tagged_data = {
            "date": self._date,
            "ticker": self._root,
            "domains": domain_to_chains(self._domains),
            "data": data,
            "header": self._header,
        }
        return tagged_data



