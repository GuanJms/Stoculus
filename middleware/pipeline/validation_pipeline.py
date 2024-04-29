from data_meta.option_meta_manager import OptionMetaManager
from middleware.requester import ThetaMetaRequester
from middleware.validator import OptionLocalValidator


class ValidationPipeline:
    def __init__(self):
        self.option_local_validator = OptionLocalValidator()
        self.option_meta_manager = OptionMetaManager()
        self.theta_meta_requester = ThetaMetaRequester()

    def validate_ticker(self, ticker: str) -> bool:
        return self.option_local_validator.check_valid_ticker(ticker)

    def get_exps(self, ticker: str) -> list:
        if not self.validate_ticker(ticker):
            return []
        return self.option_local_validator.get_exps(ticker)

    def get_strikes(self, ticker: str, exp: int) -> list:
        online_strikes = None
        if not self.validate_ticker(ticker):
            return []
        local_strikes = self.option_local_validator.get_strikes(ticker, exp)
        if local_strikes is None:
            online_strikes = self.theta_meta_requester.get_option_strikes(ticker, exp)
        if online_strikes is None:
            return []
        else:
            # update option meta with online data
            self.option_meta_manager.update_exp_meta(ticker=ticker, exp=exp, strikes=online_strikes)
            return online_strikes
