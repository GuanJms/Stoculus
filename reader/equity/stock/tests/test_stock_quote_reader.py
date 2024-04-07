import unittest

from _enums import ReaderStatus
from .._stock_quote_reader import StockQuoteReader
from _enums import ReadingStatus


class TestStockQuoteReader(unittest.TestCase):
    def setUp(self):
        test_date = 20240301
        root = 'TSLA'
        reader = StockQuoteReader(date=test_date, root=root)
        self.reader = reader
        reader.configure_file()
        reader.open_stream()

    def test_reading(self):
        reader = self.reader
        peek = reader.peek_time()
        data, status = reader._read_util_time(peek+8000)
        print(len(data))
        print(status)
        print(type(data[0]))
        print(data[0])






if __name__ == '__main__':
    unittest.main()
