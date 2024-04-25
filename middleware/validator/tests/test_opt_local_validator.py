import unittest
from middleware.validator import OptionLocalValidator


class TestOptionLocalValidator(unittest.TestCase):
    def test_directory_path(self):
        validator = OptionLocalValidator()
        path = validator.get_director_path()
        print(path)




if __name__ == '__main__':
    unittest.main()
