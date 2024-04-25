import unittest
from middleware.validator import ThetaValidator
class TestValidChecker(unittest.TestCase):
    def test_valid_ticker_api_test(self):
        root = 'TSLA'
        self.assertTrue(ThetaValidator.check_valid_ticker())

        fale_root = 'TSLAA'
        self.assertFalse(ThetaValidator.check_valid_ticker())











if __name__ == '__main__':
    unittest.main()
