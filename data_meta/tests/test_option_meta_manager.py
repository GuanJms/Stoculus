import unittest

from data_meta.option_meta_manager import OptionMetaManager


class TestOptionMetaManager(unittest.TestCase):

    def test_exp_update(self):
        manager = OptionMetaManager()
        manager.update(verbose=True)



if __name__ == '__main__':
    unittest.main()
