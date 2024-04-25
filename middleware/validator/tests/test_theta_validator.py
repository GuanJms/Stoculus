import unittest
from middleware.validator 
class TestValidChecker(unittest.TestCase):
    def test_valid_ticker_api_test(self):
        root = 'TSLA'
        self.assertTrue(ThetaValidChecker.check_valid_ticker(root))

        fale_root = 'TSLAA'
        self.assertFalse(ThetaValidChecker.check_valid_ticker(fale_root))











if __name__ == '__main__':
    unittest.main()
