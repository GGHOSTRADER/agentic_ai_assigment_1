
# You are a python agentic developer

##  Goal : You must implement best coding practices, including Function Maps for routing, Environment Variables for security, and handling Parallel Tool Calls .

### Invariants:
- Model must recieve tool schema
- Model must output the request for tools in scheme format
- Must use function mapping to call functions, Do not use long if-else chains.
- No use of higher level frameworks, agent must handle all code locally
- Must use  python-dotenv to manage API keys
- Do not fetch real data from the web, mock data will me fetch in the functions
- Context Window: The agent must remember previous turns (eg, "What is its price?" after mentioning AAPL). Pass previous messages from client and model to the model each time the model is called.
- Must supports tool calls via the OpenAI Python SDK interface


### Functions 
Function 1 Exchange Rate

```
def get_exchange_rate(currency_pair: str) --> json string:

    if currency_pair in ["USD_TWD","JPY_TWD","EUR_USD"]
        exchange_rates =  {"USD_TWD":"32.0",
        "JPY_TWD" : "0.2",
        "EUR_USD" : "1.2"}
        return {"currency_pair": currency_pair , "rate": exchange_rates[currency_pair]} 
    else
        return {"error": "Minor inconvenience, Data not found, please change your input"}
```

Function 2 Stock Prices
```
def get_stock_price(symbol: str) --> json string:
 
    if symbol in ["AAPL","TSLA,"NVDA"]:
        stock_prices = {"AAPL" : "260.00",
        "TSLA" : "430.00",
        "NVDA" : "190.00"}
        return {"symbol": symbol , "price": stock_prices[symbol]} 
    else
        return {"error": "Minor inconvenience, Data not found, please change your input"}
```
### 4. Tool Schemas
```
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_exchange_rate",
            "description": "Get exchange rate for currency pair",
            "parameters": {
                "type": "object",
                "properties": {
                    "currency_pair": {"type": "string", "description": "exchange rate between two currencies"}
                },
                "required": ["location"],
                "additionalProperties": False
            },
            "strict": True
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_stock_price",
            "description": "Get stock price",
            "parameters": {
                "type": "object",
                "properties": {
                    "symbol": {"type": "string"}
                },
                "required": ["a", "b"],
                "additionalProperties": False
            },
            "strict": True
        }
    }
]
```
### Agent initial message

```
messages = [
        {"role": "system", "content": "You are a Financial Assistant can tell exchange rate of a currency pair and prices of stocks. Use tools when needed and can request to use tools more than once if needed."}
    ]

```

### sucess criteria:

- Environment & Security
  - No API keys hardcoded in main.py 
  - requirements.txt is included and complete

- Code Structure
  - Implements a Function Map (Dictionary) for tool routing.

- Tool Definition (Schema)
  - tools list correctly defines get_exchange_rate and get_stock_price .
  - Parameters (eg, symbol ) are correctly typed.
  - Uses "strict": true or correct property constraints.

- Task A & B: Single Query
  - Exchange Rate: Queries for "USD to TWD" return 32.0 .
  - Stock Price: Queries for "NVDA" return 190.00 .

- Task C: Parallel Calls
  - Query: "Check AAPL price and JPY_TWD rate" (or similar).
  - Critical: Agent must emit two tool calls in a single turn/request.
  - Final answer integrates both results correctly.


- Task D: Memory & Persona
  - Successfully recalls user information provided in previous turns.
  - Maintains the "Financial Assistant" persona defined in the System Prompt.


- Task E: Robustness
  - Queries for unknown data (eg, "GOOG") return a polite error message (based on the mock error return).
  - The program does not crash or exit unexpectedly.