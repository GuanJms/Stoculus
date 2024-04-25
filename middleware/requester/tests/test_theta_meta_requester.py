import unittest
from middleware.requester import ThetaMetaRequester
class TestThetaMetaRequester(unittest.TestCase):
    def test_get_option_strikes(self):
        root = 'TSLA'
        exp = 20240426
        data = ThetaMetaRequester().get_option_strikes(root=root, exp=exp)
        self.assertIsNotNone(data)

    def test_get_option_expirations(self):
        root = 'TSLA'
        data = ThetaMetaRequester().get_option_expirations(root=root)
        print(data)
        self.assertIsNotNone(data)





if __name__ == '__main__':
    unittest.main()
