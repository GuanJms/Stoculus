from path import PathManager
from ._meta_manager import MetaManager
from data_meta.meta_enums import MetaEnum
from _enums import DomainEnum, AssetDomain, EquityDomain


class TickerMetaManager(MetaManager):

    OPTION_TICKER_METAS = [MetaEnum.OPTION, MetaEnum.TICKER]

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'):
            cls.instance = super(TickerMetaManager, cls).__new__(cls)
        return cls.instance

    def __init__(self, **kwargs):
        super().__init__()
        self._verbose = kwargs.get('verbose', False)
        self.load_meta()

    def load_meta(self, **kwargs):
        try:
            path = PathManager.get_meta_path(self.OPTION_TICKER_METAS)
            self.meta = self.read_json(path)
        except FileNotFoundError:
            print(f"Meta path not found for {self.OPTION_TICKER_METAS}")

    def get_meta(self):
        return self.meta

    def has_ticker(self, ticker: str):
        return ticker in self.meta

    def update(self, **kwargs):
        self.load_meta(**kwargs)
        try:
            self._update_option_ticker_meta()
        except Exception as e:
            print(f"Error updating option ticker meta - {e}")

    def _update_option_ticker_meta(self):
        path = PathManager.get_director_path([AssetDomain.EQUITY, EquityDomain.OPTION])
        tickers = self.get_directories(path)
        self.protected_folder_filter(tickers)
        meta_path = PathManager.get_meta_path(self.OPTION_TICKER_METAS)
        self.overwrite_json(meta_path, tickers)

    @staticmethod
    def protected_folder_filter(folders):
        for folder in folders:
            if folder.startswith('_'):
                folders.remove(folder)








