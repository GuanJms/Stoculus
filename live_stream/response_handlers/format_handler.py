"""
This is a formatHandler class that is responsible for formatting the response
into a format that aligns with the stoculus general format.
"""
import math

from live_stream.response_handlers.base_handler import BaseHandler
import asyncio
import websockets
import json

"""
- "data"
    - list of dictionaries of contract meta and data
- "status"

Samples
 - "data": [
    {"date": 20230602,"ticker": "TSLA","domains": "EQUITY.STOCK.QUOTE","data": [[ 1, ,2 ,3....], [,12,321,4,14]],"header": ["A", "B", "C...],},
    {"date": 20230602, "ticker": "SPY", "domains": "EQUITY.STOCK.QUOTE", "data": ..., "header": ... },...],
- "status": "DONE",
"""


def msd_to_time(msd):
    # Total seconds
    total_seconds = msd // 1000

    # Calculate hours, minutes, and seconds
    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)

    # Format the result as HH:MM:SS
    return f"{hours:02}:{minutes:02}:{seconds:02}"


# Example usage (commented out for PCI):
# print(msd_to_time(86399999))  # Should print "23:59:59"

class FormatHandler(BaseHandler):
    def __init__(self):
        super().__init__()
        self.option_quote_cache = {}
        self.stock_quote_cache = {}
        self.stock_quote_size_cache = {}
        self.option_quote_size_cache = {}

    async def process(self, response):
        # try:
        response_data = json.loads(response)
        security_type = response_data['contract']['security_type']
        header_type = response_data['header']['type']  # TRADE, QUOTE, OHLC
        match security_type:
            case "OPTION":
                match header_type:
                    case "TRADE":
                        format_response = self._format_option_trade_data(response_data)
                        self.print_colored_option_data(format_response, _type="TRADE")
                        return format_response
                    case "QUOTE":
                        format_response = self._format_option_quote_data(response_data)
                        self.print_colored_option_data(format_response, _type="QUOTE")
                        return format_response
                    case _:
                        # print(f"Option {type} data not supported")
                        pass
            case "STOCK":
                match header_type:
                    case "TRADE":
                        format_response = self._format_stock_trade_data(response_data)
                        self.print_colored_stock_data(format_response, _type="TRADE")
                        return format_response
                    case "QUOTE":
                        format_response = self._format_stock_quote_data(response_data)
                        self.print_colored_stock_data(format_response, _type="QUOTE")
                        return format_response
                    case _:
                        pass
            case _:
                pass
        # except Exception as e:
        #     print(f"Error in format handler: {e}")

    @staticmethod
    def _format_option_trade_data(response_data) -> dict:
        # Format option trade data to stoculus format
        format_response = {'date': response_data['trade']['date'], 'ticker': response_data['contract']['root'],
                           'domains': f"EQUITY.OPTION.TRADED", 'contract': response_data['contract'],
                           'data': response_data['trade'],
                           'mode': 'live'}  # Add format live for live data dictionary singleton
        return format_response

    @staticmethod
    def _format_option_quote_data(response_data) -> dict:
        format_response = {'date': response_data['quote']['date'], 'ticker': response_data['contract']['root'],
                           'domains': f"EQUITY.OPTION.QUOTE", 'contract': response_data['contract'],
                           'data': response_data['quote'],
                           'mode': 'live'}
        return format_response

    @staticmethod
    def _format_stock_trade_data(response_data) -> dict:
        format_response = {'date': response_data['trade']['date'], 'ticker': response_data['contract']['root'],
                           'domains': f"EQUITY.STOCK.TRADED", 'contract': response_data['contract'],
                           'data': response_data['trade'],
                           'mode': 'live'}  # Add format live for live data dictionary singleton
        return format_response

    def print_colored_option_data(self, option_data, _type=None, minimum_size=10):
        # print(option_data)

        if not _type:
            return
        root = option_data.get('contract', {}).get('root', '')
        size = option_data.get('data', {}).get('size', 0)
        strike = option_data.get('contract', {}).get('strike', 0)
        right = option_data.get('contract', {}).get('right', '')
        msd = option_data.get('data', {}).get('ms_of_day', 0)
        time_str = msd_to_time(msd)

        match _type:
            case "TRADE":
                price = option_data.get('data', {}).get('price', 0)

                if size > 50:
                    size_color_code = "\033[93;1m"  # Bold Yellow (Gold-like color)
                elif size > 10:
                    size_color_code = "\033[94;1m"
                else:
                    size_color_code = "\033[0m"

                right = option_data.get('contract', {}).get('right', '')
                key = (root, right)
                bid_quote = self.option_quote_cache.get(key, {}).get(strike, {}).get('bid', 0)
                ask_quote = self.option_quote_cache.get(key, {}).get(strike, {}).get('ask', 0)
                mid_quote = (bid_quote + ask_quote) / 2
                if not bid_quote or not ask_quote or round(price, 2) == round(mid_quote, 2):
                    if right == 'C':
                        direct_color_code = "\033[92m"
                    elif right == 'P':
                        direct_color_code = "\033[91m"
                    else:
                        direct_color_code = "\033[0m"
                else:
                    if right == 'C' and price > mid_quote:
                        direct_color_code = "\033[92m"  # Green
                    elif right == 'P' and price > mid_quote:
                        direct_color_code = "\033[91m"  # Red
                    elif right == 'C' and price < mid_quote:
                        direct_color_code = "\033[91m"
                    elif right == 'P' and price < mid_quote:
                        direct_color_code = "\033[92m"
                # print(f"{color_code}{option_data}\033[0m")

                bid_ask_imb_str = self.__bid_ask_imbalance_visualization_option(root, strike, right)

                if size >= minimum_size:
                    print(
                        f"{bid_ask_imb_str} || {size_color_code} size: {size}, strike: {strike},\033[0m {direct_color_code} price: {price}, strike: {strike}, right: {right}\033[0m || {time_str}  {msd}")

            case "QUOTE":
                bid = option_data.get('data', {}).get('bid', 0)
                ask = option_data.get('data', {}).get('ask', 0)
                bid_size = option_data.get('data', {}).get('bid_size', 0)
                ask_size = option_data.get('data', {}).get('ask_size', 0)

                self.update_quote_cache(root, strike, bid, ask, right)
                self.option_quote_size_cache[(root, right)] = {
                    strike: {'bid_size': bid_size, 'ask_size': ask_size}}

                direct_color_code = "\033[0m"  # Default color (no color)
                # print(f"{direct_color_code} strike: {strike}, right: {right}, bid: {bid}, ask: {ask}, bid_size: {bid_size}, ask_size: {ask_size}\033[0m")

    def print_colored_stock_data(self, format_response, _type=None, minimum_size=99):

        if not _type:
            return
        match _type:
            case "TRADE":
                root = format_response.get('contract', {}).get('root', '')
                size = format_response.get('data', {}).get('size', 0)
                price = format_response.get('data', {}).get('price', 0)
                msd = format_response.get('data', {}).get('ms_of_day', 0)
                time_str = msd_to_time(msd)
                if size >= 1000:  # light blue
                    size_color_code = "\033[93;1m"
                elif size >= 200:  # light blue
                    size_color_code = "\033[94;1m"
                else:
                    size_color_code = "\033[0m"

                mid_quote = self.stock_quote_cache.get(root, {}).get('mid', 0)
                if not mid_quote or round(price, 2) == round(mid_quote, 2):
                    direct_color_code = "\033[0m"
                else:
                    if price > mid_quote:
                        direct_color_code = "\033[92m"  # Green
                    else:
                        direct_color_code = "\033[91m"  # Red
                order_type = 'SELL' if price < mid_quote else 'BUY'
                bid_ask_imbalance_vis = self._bid_ask_imbalance_visualization_stock(root, traded_size=size,
                                                                                    order_type=order_type)
                bid_ask_market_impact_vis = self._bid_ask_price_impact_visualization_stock(root, price)

                if size >= minimum_size:
                    print(
                        f"{bid_ask_imbalance_vis} || {size_color_code} size: {size},\033[0m {direct_color_code} price: {price}\033[0m"
                        f" || {bid_ask_market_impact_vis} || {time_str}")
            case "QUOTE":
                root = format_response.get('contract', {}).get('root', '')
                bid = format_response.get('data', {}).get('bid', 0)
                ask = format_response.get('data', {}).get('ask', 0)
                bid_size = format_response.get('data', {}).get('bid_size', 0)
                ask_size = format_response.get('data', {}).get('ask_size', 0)
                self.stock_quote_cache[root] = {'bid': bid, 'ask': ask, 'mid': (bid + ask) / 2}
                self.stock_quote_size_cache[root] = {'bid_size': bid_size, 'ask_size': ask_size}

    def update_quote_cache(self, root, strike, bid, ask, right):
        if root not in self.option_quote_cache:
            self.option_quote_cache[(root, right)] = {}
        self.option_quote_cache[(root, right)][strike] = {'bid': bid, 'ask': ask}

    @staticmethod
    def _format_stock_quote_data(response_data) -> dict:
        format_response = {'date': response_data['quote']['date'], 'ticker': response_data['contract']['root'],
                           'domains': f"EQUITY.STOCK.QUOTE", 'contract': response_data['contract'],
                           'data': response_data['quote'],
                           'mode': 'live'}
        return format_response

    def __bid_ask_imbalance_visualization_option(self, root, strike, right, dash_length=20):
        bid_size = self.option_quote_size_cache.get((root, right), {}).get(strike, {}).get('bid_size', 0)
        ask_size = self.option_quote_size_cache.get((root, right), {}).get(strike, {}).get('ask_size', 0)
        if bid_size == 0 and ask_size == 0:
            return "-" * dash_length
        ratio = bid_size / (bid_size + ask_size)

        if right == 'P':
            ratio = 1 - ratio

        # print(f"__bid_ask_imbalance_visualization_option ratio: {ratio}")
        resistance_color_code = self.get_resistance_color_code(ratio)

        bid_dash = int(ratio * dash_length)
        ask_dash = dash_length - bid_dash
        return f"{resistance_color_code}{'=' * bid_dash}|{'-' * ask_dash}\033[0m"

    def _bid_ask_imbalance_visualization_stock(self, root, dash_unit=10, max_dash=40, traded_size=0,
                                               order_type=None) -> str:
        bid_size = self.stock_quote_size_cache.get(root, {}).get('bid_size', 0)
        ask_size = self.stock_quote_size_cache.get(root, {}).get('ask_size', 0)
        if bid_size == 0 and ask_size == 0:
            return "-" * max_dash
        traded_size = min(traded_size / 1.5, 200)
        bid_ratio = bid_size / (bid_size + ask_size + traded_size)
        ask_ratio = ask_size / (bid_size + ask_size + traded_size)
        total_size = bid_size + ask_size + traded_size
        bid_book_ratio = bid_size / (bid_size + ask_size)

        dash_length = total_size // dash_unit
        if dash_length > max_dash:
            dash_length = max_dash

        # sell dash and buy dash
        transaction_dash = 0
        if order_type is None:
            transaction_dash = int(traded_size / total_size * dash_length)
            buy_dash = 0
            sell_dash = 0
        if order_type == "SELL":
            sell_dash = int(traded_size / total_size * dash_length)
            buy_dash = 0
        else:
            buy_dash = int(traded_size / total_size * dash_length)
            sell_dash = 0

        filler = max_dash - dash_length
        half_dash = int(filler // 2)

        resistance_color_code = self.get_resistance_color_code(bid_book_ratio)

        bid_dash = int(bid_ratio * dash_length)
        ask_dash = int(ask_ratio * dash_length)

        return (f"{resistance_color_code}{' ' * half_dash}{'=' * bid_dash}\033[0m"
                f"{self.color_str('|' * sell_dash, color_str='RED')}"
                f"{'|' * transaction_dash}"
                f"{self.color_str('|' * buy_dash, color_str='GREEN')}"
                f"{resistance_color_code}{'-' * ask_dash}{' ' * half_dash}\033[0m")

    @staticmethod
    def color_str(text, color_code=None, color_str=None):
        if color_str == 'RED':
            color_code = "\033[91m"
        elif color_str == 'GREEN':
            color_code = "\033[92m"
        return f"{color_code}{text}\033[0m"

    @staticmethod
    def get_resistance_color_code(ratio):
        if ratio > 0.5:
            # Shades of green from dark to light
            shades_of_green = [28, 34, 40, 46, 82, 118]
            index = math.floor((ratio - 0.5) * 2 * (len(shades_of_green) - 1))
            return f"\033[38;5;{shades_of_green[index]}m"
        elif ratio <= 0.5:
            # Lighter shades of red
            shades_of_red = [174, 181, 196, 203, 210, 217]
            index = math.floor(ratio * 2 * (len(shades_of_red) - 1))
            # print(f"index: {index}")
            return f"\033[38;5;{shades_of_red[index]}m"
        else:
            print("Invalid ratio")
            raise ValueError("Invalid ratio")

    def _bid_ask_price_impact_visualization_stock(self, root, price, max_length=40, unit=0.05):
        bid_price = self.stock_quote_cache.get(root, {}).get('bid', 0)
        ask_price = self.stock_quote_cache.get(root, {}).get('ask', 0)
        negative_market_impact_ratio = max(min((price - bid_price) / (ask_price - bid_price), 1.0), 0.0)
        spread = ask_price - bid_price
        dash_length = int(spread * max_length / unit)
        left_dash = int((price - bid_price) / (ask_price - bid_price) * dash_length)
        right_dash = dash_length - left_dash
        color_code = self.get_resistance_color_code(negative_market_impact_ratio)
        return f"{color_code}{'=' * left_dash}|{'-' * right_dash}\033[0m"


"""
-- option trade data
Received: {"header":{"type":"OHLC","status":"CONNECTED"},
"contract":{"security_type":"OPTION","root":"NVDA","expiration":20240524,"strike":950000,"right":"C"},
"ohlc":{"ms_of_day":45178870,"open":35.55,"high":41.6,"low":33.35,"close":40.1,"volume":11341,"count":4711,"date":20240521}}
Received: {"header":{"type":"TRADE","status":"CONNECTED"},
    "contract":{"security_type":"OPTION","root":"NVDA","expiration":20240524,"strike":950000,"right":"C"},
    "trade":{"ms_of_day":45173736,"sequence":780839941,"size":1,"condition":130,"price":39.99,"exchange":65,"date":20240521}}
Received: {"header":{"type":"QUOTE","status":"CONNECTED"},
    "contract":{"security_type":"OPTION","root":"NVDA","expiration":20240524,"strike":950000,"right":"C"},
    "quote":{"ms_of_day":45178850,"bid_size":18,"bid_exchange":43,"bid":39.9,"bid_condition":50,"ask_size":1,"ask_exchange":7,"ask":40.1,"ask_condition":50,"date":20240521}}


-- stock trade data
Sample of the response from the theta data server
Received: {"header":{"type":"TRADE","status":"CONNECTED"},
    "contract":{"security_type":"STOCK","root":"NVDA"},
    "trade":{"ms_of_day":39657065,"sequence":11529167,"size":1,"condition":115,"price":947.51,"exchange":57,"date":20240521}}
Received: {"header":{"type":"QUOTE","status":"CONNECTED"},
    "contract":{"security_type":"STOCK","root":"NVDA"},
    "quote":{"ms_of_day":39655484,"bid_size":50,"bid_exchange":29,"bid":947.3,"bid_condition":0,"ask_size":6,"ask_exchange":29,"ask":947.44,"ask_condition":0,"date":20240521}}
Received: {"header":{"type":"OHLC","status":"CONNECTED"},
    "contract":{"security_type":"STOCK","root":"NVDA"},
    "ohlc":{"ms_of_day":39657065,"open":953.85,"high":956.6,"low":931.55,"close":947.51,"volume":10046138,"count":244304,"date":20240521}}





"""
