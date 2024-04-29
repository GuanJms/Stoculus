import unittest
from unittest import TestCase
from middleware.pipeline.validation_pipeline import ValidationPipeline


class TestValidationPipeline(TestCase):

    def test_validate_ticker(self):
        pipeline = ValidationPipeline()
        assert pipeline.validate_ticker('SPY') == True
        assert pipeline.validate_ticker('INVALID') == False

    def test_get_exps(self):
        pipeline = ValidationPipeline()
        assert len(pipeline.get_exps('SPY')) > 0
        assert len(pipeline.get_exps('INVALID')) == 0

        print(pipeline.get_exps('SPY'))

    def test_get_strikes(self):
        pipeline = ValidationPipeline()
        data = pipeline.get_strikes('SPY',20240506)
        assert len(data) > 0
        print(data)



if __name__ == '__main__':
    unittest.main()
