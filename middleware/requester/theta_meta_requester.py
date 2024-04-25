from middleware.requester._theta_requester import ThetaRequester


class ThetaMetaRequester(ThetaRequester):

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'):
            cls.instance = super(ThetaMetaRequester, cls).__new__(cls)
        return cls.instance

    def get_option_root_listing(self):
        _url = self.url + '/list/roots/option'
        return self.get_request(_url)

    def get_stock_root_listing(self):
        _url = self.url + '/list/roots/option'
        return self.get_request(_url)

    def get_option_expirations(self, root: str):
        _url = self.url + f'/list/expirations'
        return self.get_request(_url, params={'root': root})


    def get_option_strikes(self, root: str, exp: int):
        _url = self.url + f'/list/strikes'
        return self.get_request(_url, params={'root': root, 'exp': exp})
