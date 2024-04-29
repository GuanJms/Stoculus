from pathlib import Path
from typing import List

from _enums import DomainEnum
from configuration import ConfigurationManager
from utils._time_operations import get_month_string


def check_path_exists(path_str: str) -> bool:
    return Path(path_str).exists()


def check_path_exists_error(path: Path, error_message: str | None = None):
    if not path.exists():
        raise FileNotFoundError(f"File not found: {path} {error_message if error_message else ''}")


def get_stock_quote_path(**kwargs):
    if 'root' not in kwargs:
        raise ValueError('Root is required')
    if 'date' not in kwargs:
        raise ValueError('Date is required')

    domains = kwargs.get('domains')
    root = kwargs.get('root')
    date = kwargs.get('date')
    if isinstance(date, int):
        date = str(date)
    year = date[0:4]
    month = date[4:6]
    file_type = kwargs.get('file_type')
    file_name = f'{date}.{file_type}'
    DATABASE_ROOT = Path(ConfigurationManager.get_root_system())
    DOMAIN_PATH = ConfigurationManager.get_domain_path(domains)

    path = DATABASE_ROOT / DOMAIN_PATH['EQUITY'] / DOMAIN_PATH['STOCK'] / root / DOMAIN_PATH[
        'QUOTE'] / year / month / file_name
    check_path_exists_error(path)
    return path


def get_option_eod_path(**kwargs) -> Path:
    domains = kwargs.get('domains')
    root = kwargs.get('root')
    exp = kwargs.get('exp')
    year = kwargs.get('year')
    month = kwargs.get('month')
    if isinstance(exp, int):
        exp = str(exp)
    year = str(year)
    month = get_month_string(month)

    file_type = kwargs.get('file_type')
    file_name = f'{exp}.{file_type}'
    DATABASE_ROOT = Path(ConfigurationManager.get_root_system())
    DOMAIN_PATH = ConfigurationManager.get_domain_path(domains)

    path = (DATABASE_ROOT / DOMAIN_PATH['EQUITY'] / DOMAIN_PATH['OPTION'] / root /
            DOMAIN_PATH['EOD'] / year / month / file_name)
    check_path_exists_error(path)
    return path


def get_directory_path(domains: List[DomainEnum], **kwargs) -> Path:
    DATABASE_ROOT = Path(ConfigurationManager.get_root_system())
    DOMAIN_PATH = ConfigurationManager.get_domain_path(domains)
    path = DATABASE_ROOT
    for domain in domains:
        path = path / DOMAIN_PATH[domain.name]
    check_path_exists_error(path)
    return path


def get_meta_path(metas: List[DomainEnum], **kwargs) -> Path:
    META_ROOT = Path(ConfigurationManager.get_root_system()) / ConfigurationManager.get_meta_path()
    META_PATH = ConfigurationManager.get_meta_config(metas)
    path = META_ROOT
    for meta in metas:
        path = path / META_PATH[meta.name]
    create_meta_json_file_if_not_exists(path)
    return path


def create_meta_json_file_if_not_exists(path: Path):
    if not path.exists():
        with open(path, 'w') as file:
            file.write('{}')


def get_stock_traded_path(**kwargs):
    return None


def get_option_quote_path(**kwargs):
    return None


def get_option_traded_quote_path(**kwargs):
    return None
