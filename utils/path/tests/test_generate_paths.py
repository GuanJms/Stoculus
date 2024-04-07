import unittest
from .._generate_paths import *


class TestGeneratePathFunctions(unittest.TestCase):
    def test_get_stock_quote_path(self):
        root = 'TSLA'
        date = '20240301'
        print(get_stock_quote_path(root=root, date=date, domains=['EQUITY', 'STOCK', 'QUOTE']))


if __name__ == '__main__':
    unittest.main()
