"""
functions.py

This module contains the financial functions for the agent:
- get_exchange_rate: Retrieves exchange rate for currency pairs
- get_stock_price: Retrieves stock prices for symbols

It also defines the available_functions map for dynamic function routing.
"""

import json


def get_exchange_rate(currency_pair: str) -> str:
    """
    Get the exchange rate for a given currency pair.

    Args:
        currency_pair (str): The currency pair, e.g., "USD_TWD"

    Returns:
        str: JSON string containing the currency pair and rate, or an error message
    """
    if currency_pair in ["USD_TWD", "JPY_TWD", "EUR_USD"]:
        exchange_rates = {"USD_TWD": "32.0", "JPY_TWD": "0.2", "EUR_USD": "1.2"}
        return json.dumps(
            {"currency_pair": currency_pair, "rate": exchange_rates[currency_pair]}
        )
    else:
        return json.dumps(
            {
                "error": "Minor inconvenience, Data not found, Request to change the input please ***DO NOT SUGGEST OTHER PAIRS***"
            }
        )


def get_stock_price(symbol: str) -> str:
    """
    Get the stock price for a given symbol.

    Args:
        symbol (str): The stock symbol, e.g., "AAPL"

    Returns:
        str: JSON string containing the symbol and price, or an error message
    """
    if symbol in ["AAPL", "TSLA", "NVDA"]:
        stock_prices = {"AAPL": "260.00", "TSLA": "430.00", "NVDA": "190.00"}
        return json.dumps({"symbol": symbol, "price": stock_prices[symbol]})
    else:
        return json.dumps(
            {
                "error": "Minor inconvenience, Data not found, Request to change the input please ***DO NOT SUGGEST OTHER TICKERS***"
            }
        )


# Function Map for dynamic routing
available_functions = {
    "get_exchange_rate": get_exchange_rate,
    "get_stock_price": get_stock_price,
}
