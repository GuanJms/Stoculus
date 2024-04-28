import unittest

from data_meta.ticker_meta_manager import TickerMetaManager


class TestTickerMetaManager(unittest.TestCase):
    def test_root_loading(self):
        manager = TickerMetaManager()
        tickers = manager._update_option_ticker_meta()
        print(tickers)
        # manager.update()




if __name__ == '__main__':
    unittest.main()
