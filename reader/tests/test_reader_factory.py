import unittest
from reader import ReaderFactory

class TestReaderFactory(unittest.TestCase):
    def test_reader_factory(self):
        reader = ReaderFactory.create_reader(domain_chain_str='EQUITY.STOCK.QUOTE', root = 'TSLA', date = 20240301)
        reader.configure_file()
        reader.open_stream()
        peek = reader.peek_time()
        data, status = reader._read_upto_time(peek + 8000)
        print(data)
        print(status)



if __name__ == '__main__':
    unittest.main()
