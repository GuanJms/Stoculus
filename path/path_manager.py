from typing import Optional

from data_meta.meta_enums import MetaEnum
from path._generate_paths import *
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
        domain_map = kwargs.get('domain_map', None)
        if len(domains) == 0:
            raise ValueError('domains cannot be empty')

        domain_action_str = DomainMatcher.match_domain(domains, domain_map=domain_map)
        domain_action = path_action_map[domain_action_str]
        return domain_action(domains=domains, **kwargs)

    @staticmethod
    def get_director_path(domains: List[DomainEnum], **kwargs) -> Optional[Path]:
        if len(domains) == 0:
            raise ValueError('domains cannot be empty')
        path = get_directory_path(domains, **kwargs)
        return path

    @staticmethod
    def get_meta_path(metas: List[MetaEnum], **kwargs) -> Optional[Path]:
        if len(metas) == 0:
            raise ValueError('metas cannot be empty')
        path = get_meta_path(metas, **kwargs)
        return path