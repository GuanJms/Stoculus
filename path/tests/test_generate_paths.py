import unittest
from path._generate_paths import *
from _enums import *


class TestGeneratePathFunctions(unittest.TestCase):
    def test_get_stock_quote_path(self):
        root = 'TSLA'
        date = '20240301'
        domains = [AssetDomain.EQUITY, EquityDomain.STOCK, PriceDomain.QUOTE]
        file_type = 'csv'
        print(get_stock_quote_path(root=root, date=date, domains=domains, file_type=file_type))

    def test_get_directory_path(self):
        domains = [AssetDomain.EQUITY, EquityDomain.OPTION]
        print(get_directory_path(domains=domains))


if __name__ == '__main__':
    unittest.main()
