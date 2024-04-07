from pathlib import Path

from configuration import ConfigurationManager


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


def get_stock_traded_path(**kwargs):
    return None


def get_option_quote_path(**kwargs):
    return None


def get_option_traded_quote_path(**kwargs):
    return None
