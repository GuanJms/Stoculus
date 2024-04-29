import unittest

from data_meta.option_meta_manager import OptionMetaManager


class TestOptionMetaManager(unittest.TestCase):

    def test_exp_update(self):
        manager = OptionMetaManager()
        manager.update(verbose=True)

    def test_get_option_meta(self):
        manager = OptionMetaManager()
        print(manager.get_option_meta('SPY'))



if __name__ == '__main__':
    unittest.main()
