# sai/bot/trader.py

import logging
import os
import alpaca_trade_api as tradeapi
from binance.client import Client as BinanceClient

class Trader:
    def __init__(self, broker="alpaca"):
        self.broker = broker.lower()

        if self.broker == "alpaca":
            self.api_key = os.getenv("ALPACA_API_KEY")
            self.secret_key = os.getenv("ALPACA_SECRET_KEY")
            self.base_url = os.getenv("ALPACA_BASE_URL", "https://paper-api.alpaca.markets")

            if not self.api_key or not self.secret_key:
                raise ValueError("Missing Alpaca API credentials")

            self.api = tradeapi.REST(self.api_key, self.secret_key, self.base_url)

        elif self.broker == "binance":
            self.api_key = os.getenv("BINANCE_API_KEY")
            self.secret_key = os.getenv("BINANCE_SECRET_KEY")

            if not self.api_key or not self.secret_key:
                raise ValueError("Missing Binance API credentials")

            self.api = BinanceClient(self.api_key, self.secret_key)

        else:
            raise ValueError(f"Unsupported broker: {broker}")

    def execute(self, action, data):
        symbol = data.get("symbol", "AAPL" if self.broker == "alpaca" else "BTCUSDT")
        qty = data.get("qty", 1)

        try:
            if self.broker == "alpaca":
                if action == "BUY":
                    order = self.api.submit_order(
                        symbol=symbol, qty=qty, side="buy",
                        type="market", time_in_force="gtc"
                    )
                elif action == "SELL":
                    order = self.api.submit_order(
                        symbol=symbol, qty=qty, side="sell",
                        type="market", time_in_force="gtc"
                    )
                else:
                    return {"status": "ignored", "action": action}
                return {"status": "success", "order_id": order.id, "symbol": symbol, "qty": qty}

            elif self.broker == "binance":
                if action == "BUY":
                    order = self.api.order_market_buy(symbol=symbol, quantity=qty)
                elif action == "SELL":
                    order = self.api.order_market_sell(symbol=symbol, quantity=qty)
                else:
                    return {"status": "ignored", "action": action}
                return {"status": "success", "order_id": order["orderId"], "symbol": symbol, "qty": qty}

        except Exception as e:
            logging.error(f"Trade execution failed: {e}", exc_info=True)
            return {"status": "error", "error": str(e)}

def evaluate_trade(entry_price, exit_price, direction):
    if direction == "buy":
        return exit_price - entry_price
    else:
        return entry_price - exit_price
