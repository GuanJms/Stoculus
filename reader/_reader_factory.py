from typing import Optional

from _enums import DomainEnum
from utils._domain_operations import parse_domain
from utils import DomainMatcher
from .equity.stock import StockQuoteReader

reader_action_map = {
    'get_stock_quote': StockQuoteReader
}


class ReaderFactory:

    @staticmethod
    def create_reader(domain_chain_str: Optional[str] = None, domains: Optional[DomainEnum] = None, **kwargs):
        if domain_chain_str is None and domains is None:
            raise ValueError('domain_chain_str or domains is required')
        if domain_chain_str is not None:
            domains = parse_domain(domain_chain_str)
            if len(domains) == 0:
                raise ValueError('domains cannot be empty')
        domain_action_str = DomainMatcher.match_domain(domains)
        reader_class = reader_action_map[domain_action_str]
        return reader_class(**kwargs)
