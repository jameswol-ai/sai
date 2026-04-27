# sai/bot/trader.py

import logging
import alpaca_trade_api as tradeapi
import os

class Trader:
    def __init__(self):
        # Load credentials from environment variables or .env
        self.api_key = os.getenv("ALPACA_API_KEY")
        self.secret_key = os.getenv("ALPACA_SECRET_KEY")
        self.base_url = os.getenv("ALPACA_BASE_URL", "https://paper-api.alpaca.markets")

        if not self.api_key or not self.secret_key:
            raise ValueError("Missing Alpaca API credentials")

        # Initialize Alpaca client
        self.api = tradeapi.REST(self.api_key, self.secret_key, self.base_url)

    def execute(self, action, data):
        """Place a trade based on action and market data."""
        symbol = data.get("symbol", "AAPL")   # default to AAPL if none provided
        qty = data.get("qty", 1)

        try:
            if action == "BUY":
                order = self.api.submit_order(
                    symbol=symbol,
                    qty=qty,
                    side="buy",
                    type="market",
                    time_in_force="gtc"
                )
            elif action == "SELL":
                order = self.api.submit_order(
                    symbol=symbol,
                    qty=qty,
                    side="sell",
                    type="market",
                    time_in_force="gtc"
                )
            else:
                return {"status": "ignored", "action": action}

            logging.info(f"Placed {action} order: {order}")
            return {"status": "success", "order_id": order.id, "symbol": symbol, "qty": qty}

        except Exception as e:
            logging.error(f"Trade execution failed: {e}", exc_info=True)
            return {"status": "error", "error": str(e)}
