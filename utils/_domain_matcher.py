from typing import List

from _enums import DomainEnum, AssetDomain, EquityDomain, PriceDomain

DOMAIN_MAP = {
    AssetDomain.EQUITY: {
        EquityDomain.STOCK: {
            PriceDomain.TRADED: 'get_stock_traded',
            PriceDomain.QUOTE: 'get_stock_quote'
        },
        EquityDomain.OPTION: {
            PriceDomain.TRADED: 'get_option_traded',
            PriceDomain.QUOTE: 'get_option_quote',
            PriceDomain.EOD: 'get_option_eod'
        }
    }
}


class DomainMatcher:
    @staticmethod
    def get_domain_iterator(domains: List[DomainEnum]):
        # TODO: sort the domains
        return iter(domains)

    @staticmethod
    def match_domain(domains: List[DomainEnum | AssetDomain], domain_map: dict = None, **kwargs):
        if domain_map is None:
            domain_map = DOMAIN_MAP  # default domain map
        if isinstance(domain_map, str):
            return domain_map
        domains = domains.copy()
        if domains[0] in domain_map:
            domain_map = domain_map[domains[0]]
            return DomainMatcher.match_domain(domains[1:], domain_map, **kwargs)
        else:
            raise ValueError(f'Invalid Asset Domain {domains[0]}')
