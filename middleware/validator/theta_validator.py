class ThetaValidator:

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'):
            cls.instance = super(ThetaValidator, cls).__new__(cls)
        return cls.instance

    @staticmethod
    def check_valid_ticker(root: str):
        from middleware.requester import ThetaMetaRequester
        requester = ThetaMetaRequester()
        tickers = requester.get_option_root_listing()
        if tickers is None:
            raise ValueError("Failed to get tickers")
        return root in tickers

    # @staticmethod
    # def check_valid_exp_date(root: str, exp: int):
    #     from middleware.requester import ThetaMetaRequester
    #     from middleware.validator import LocalValidator
    #
    #     requester = ThetaMetaRequester()
