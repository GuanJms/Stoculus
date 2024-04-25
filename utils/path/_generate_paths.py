from pathlib import Path

from configuration import ConfigurationManager
from utils._time_operations import get_month_string

def check_path_exists(path):
    return Path(path).exists()


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

    stock_quote_path = DATABASE_ROOT / DOMAIN_PATH['EQUITY'] / DOMAIN_PATH['STOCK'] / root / DOMAIN_PATH[
        'QUOTE'] / year / month / file_name
    path = Path(stock_quote_path)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {stock_quote_path}")
    return stock_quote_path


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

    option_eod_path = (DATABASE_ROOT / DOMAIN_PATH['EQUITY'] / DOMAIN_PATH['OPTION'] / root /
                       DOMAIN_PATH['EOD'] / year / month / file_name)

    path = Path(option_eod_path)

    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")
    return path


def get_stock_traded_path(**kwargs):
    return None


def get_option_quote_path(**kwargs):
    return None

def get_option_traded_quote_path(**kwargs):
    return None
