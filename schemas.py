"""
schemas.py

This module defines the tool schemas for the OpenAI API.
It includes schemas for get_exchange_rate and get_stock_price functions.
"""

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_exchange_rate",
            "description": "Get exchange rate for currency pair",
            "parameters": {
                "type": "object",
                "properties": {
                    "currency_pair": {
                        "type": "string",
                        "description": "exchange rate between two currencies, syntax is  short notation for currency currency1_currency2, e.g. USD_TWD, JPY_TWD, EUR_USD",
                    }
                },
                "required": ["currency_pair"],
                "additionalProperties": False,
            },
            "strict": True,
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_stock_price",
            "description": "Get stock price",
            "parameters": {
                "type": "object",
                "properties": {
                    "symbol": {"type": "string", "description": "stock symbol"}
                },
                "required": ["symbol"],
                "additionalProperties": False,
            },
            "strict": True,
        },
    },
]
