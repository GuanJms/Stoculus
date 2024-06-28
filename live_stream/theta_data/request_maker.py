class RequestMaker:

    ids = {}
    contracts = {}
    last_id = 0

    @classmethod
    def get_id(cls):
        cls.last_id += 1
        return cls.last_id

    @classmethod
    def create_option_request(cls, req_type, root, expiration, strike, right, subscribe=True):
        if req_type not in ['QUOTE', 'TRADE']:
            raise ValueError('req_type must be one of ["QUOTE", "TRADE"]')
        strike = str(strike) if not isinstance(strike, str) else strike
        expiration = str(expiration) if not isinstance(expiration, str) else expiration
        req = {'msg_type': 'STREAM', 'sec_type': 'OPTION', 'req_type': req_type, 'add': subscribe, 'id': cls.get_id(),
               'contract': {}}
        req['contract']['root'] = root
        req['contract']['expiration'] = expiration
        req['contract']['strike'] = strike
        req['contract']['right'] = right
        cls.contracts[req['id']] = req['contract']
        return req

    @classmethod
    def create_stock_request(cls, req_type, root, subscribe=True):
        req = {'msg_type': 'STREAM', 'sec_type': 'STOCK', 'req_type': req_type, 'add': subscribe, 'id': cls.get_id(),
               'contract': {}}
        req['contract']['root'] = root
        cls.contracts[req['id']] = req['contract']
        return req

    @classmethod
    def create_unsubscribe_all_request(cls):
        req = {}
        req['msg_type'] = 'STOP'
        cls.contracts = {}
        return req


