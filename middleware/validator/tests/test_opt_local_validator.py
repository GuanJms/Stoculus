import unittest
from middleware.validator import OptionLocalValidator


class TestOptionLocalValidator(unittest.TestCase):
    def test_directory_path(self):
        validator = OptionLocalValidator()
        path = validator.get_director_path()
        print(path)


    def test_valid_ticker(self):
        validator = OptionLocalValidator()
        self.assertTrue(validator.check_valid_ticker('SPY'))
        self.assertFalse(validator.check_valid_ticker('INVALID'))

    def test_option_meta(self):
        validator = OptionLocalValidator()
        exps = validator.get_exps('SPY')
        strikes = validator.get_strikes('SPY', 161)
        print(len(exps))
        print(strikes)



if __name__ == '__main__':
    unittest.main()
