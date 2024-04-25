from enum import Enum
from pathlib import Path
from typing import List, Optional

from _enums import AssetDomain, EquityDomain, PriceDomain, DomainEnum
from utils.path._generate_paths import get_stock_quote_path, get_stock_traded_path, get_option_quote_path, \
    get_option_traded_quote_path, get_option_eod_path
from utils import DomainMatcher

path_action_map = {
    'get_stock_traded': get_stock_traded_path,
    'get_stock_quote': get_stock_quote_path,
    'get_option_traded': get_option_traded_quote_path,
    'get_option_quote': get_option_quote_path,
    'get_option_eod': get_option_eod_path,
}


class PathManager:

    @staticmethod
    def get_path(domains: List[DomainEnum], **kwargs) -> Optional[Path]:
        if len(domains) == 0:
            raise ValueError('domains cannot be empty')

        domain_action_str = DomainMatcher.match_domain(domains)
        domain_action = path_action_map[domain_action_str]
        return domain_action(domains = domains, **kwargs)

    #
    #
    #     try:
    #         match domain := domain_iterator.__next__():
    #             case AssetDomain.EQUITY:
    #                 return PathManager._match_equity_domain(domain_iterator, domains=domains, **kwargs)
    #             case _:
    #                 raise ValueError(f'Invalid Asset Domain {domain}')
    #     except Exception as e:
    #         if isinstance(e, StopIteration):
    #             print('Domain is not complete')
    #         else:
    #             print(e)
    #         return None
    #
    # @staticmethod
    # def _match_equity_domain(domain_iterator, **kwargs) -> Path:
    #     match domain := domain_iterator.__next__():
    #         case EquityDomain.STOCK:
    #             return PathManager._match_stock_domain(domain_iterator, **kwargs)
    #         case EquityDomain.OPTION:
    #             return PathManager._match_option_domain(domain_iterator, **kwargs)
    #         case _:
    #             raise ValueError(f'Invalid Equity Domain{domain}')
    #
    # @staticmethod
    # def _match_stock_domain(domain_iterator, **kwargs) -> Path:
    #     match domain := domain_iterator.__next__():
    #         case PriceDomain.TRADED:
    #             return get_stock_traded_path(**kwargs)
    #         case PriceDomain.QUOTE:
    #             return get_stock_quote_path(**kwargs)
    #         case _:
    #             raise ValueError(f'Invalid Price Domain{domain}')
    #
    # @staticmethod
    # def _match_option_domain(domain_iterator, **kwargs) -> Path:
    #     match domain := domain_iterator.__next__():
    #         case PriceDomain.TRADED:
    #             return get_option_traded_quote_path(**kwargs)
    #         case PriceDomain.QUOTE:
    #             return get_option_quote_path(**kwargs)
    #         case _:
    #             raise ValueError(f'Invalid Price Domain{domain}')
