from enum import Enum
from pathlib import Path
from typing import List, Optional

from _enums import AssetDomain, EquityDomain, PriceDomain
from utils.path._generate_paths import get_stock_quote_path, get_stock_traded_path, get_option_quote_path, \
    get_option_traded_quote_path


class PathManager:

    @staticmethod
    def get_domain_iterator(domains: List[Enum]):
        # TODO: sort the domains
        return iter(domains)

    @staticmethod
    def get_path(domains: List[Enum], **kwargs) -> Optional[Path]:
        if len(domains) == 0:
            raise ValueError('domains cannot be empty')
        domain_iterator = iter(domains)
        try:
            match domain := domain_iterator.__next__():
                case AssetDomain.EQUITY:
                    return PathManager._match_equity_domain(domain_iterator, domains=domains, **kwargs)
                case _:
                    raise ValueError(f'Invalid Asset Domain {domain}')
        except Exception as e:
            if isinstance(e, StopIteration):
                print('Domain is not complete')
            else:
                print(e)
            return None

    @staticmethod
    def _match_equity_domain(domain_iterator, **kwargs) -> Path:
        match domain := domain_iterator.__next__():
            case EquityDomain.STOCK:
                return PathManager._match_stock_domain(domain_iterator, **kwargs)
            case EquityDomain.OPTION:
                return PathManager._match_option_domain(domain_iterator, **kwargs)
            case _:
                raise ValueError(f'Invalid Equity Domain{domain}')

    @staticmethod
    def _match_stock_domain(domain_iterator, **kwargs) -> Path:
        match domain := domain_iterator.__next__():
            case PriceDomain.TRADED:
                return get_stock_traded_path(**kwargs)
            case PriceDomain.QUOTE:
                return get_stock_quote_path(**kwargs)
            case _:
                raise ValueError(f'Invalid Price Domain{domain}')

    @staticmethod
    def _match_option_domain(domain_iterator, **kwargs) -> Path:
        match domain := domain_iterator.__next__():
            case PriceDomain.TRADED:
                return get_option_traded_quote_path(**kwargs)
            case PriceDomain.QUOTE:
                return get_option_quote_path(**kwargs)
            case _:
                raise ValueError(f'Invalid Price Domain{domain}')
