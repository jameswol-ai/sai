import streamlit as st
import os, random
from typing import Dict, List
from datetime import datetime
from data.database import save_account, save_positions, save_orders

class TradingAPI:
    def get_account_summary(self) -> Dict: raise NotImplementedError
    def place_order(self, symbol, units, stop_loss=None, take_profit=None, order_type="MARKET") -> Dict: raise NotImplementedError
    def get_open_positions(self) -> List[Dict]: raise NotImplementedError
    def get_order_history(self) -> List[Dict]: raise NotImplementedError

class SimulatedTrading(TradingAPI):
    def __init__(self, account):
        self.account = account
    def get_account_summary(self):
        return {"balance": self.account["balance"], "equity": self.account["equity"],
                "open_positions": len(self.account["open_positions"]),
                "unrealized_pl": 0, "margin_used": 0}
    def place_order(self, symbol, units, stop_loss=None, take_profit=None, order_type="MARKET"):
        rate = st.session_state.rates.get(symbol, 1.0)
        order = {
            "id": len(self.account["order_history"]) + 1,
            "time": datetime.now().isoformat(), "symbol": symbol, "units": units,
            "type": order_type, "price": rate,
            "stop_loss": stop_loss, "take_profit": take_profit, "status": "FILLED"
        }
        self.account["open_positions"].append(order)
        self.account["order_history"].append(order)
        self.account["equity"] = self.account["balance"]
        save_account(self.account["balance"], self.account["equity"])
        save_positions(self.account["open_positions"])
        save_orders(self.account["order_history"])
        return order
    def get_open_positions(self):
        return self.account["open_positions"]
    def get_order_history(self):
        return self.account["order_history"]
    def close_position(self, position_id):
        for p in self.account["open_positions"]:
            if p["id"] == position_id:
                self.account["open_positions"].remove(p)
                pnl = random.uniform(-50, 50)
                self.account["balance"] += pnl
                self.account["equity"] = self.account["balance"]
                p["status"] = "CLOSED"
                p["pnl"] = pnl
                self.account["order_history"].append(p)
                save_account(self.account["balance"], self.account["equity"])
                save_positions(self.account["open_positions"])
                save_orders(self.account["order_history"])
                return True
        return False

class OANDA_Trading(TradingAPI):
    def __init__(self, ctx, account_id):
        self.ctx = ctx
        self.account_id = account_id
    def get_account_summary(self):
        resp = self.ctx.account.get(self.account_id)
        if resp.status != 200:
            raise Exception(f"OANDA error: {resp.body}")
        acc = resp.body["account"]
        return {"balance": float(acc["balance"]),
                "equity": float(acc["NAV"]),
                "open_positions": acc.get("openPositionCount", 0),
                "unrealized_pl": float(acc.get("unrealizedPL", 0)),
                "margin_used": float(acc.get("marginUsed", 0))}
    def place_order(self, symbol, units, stop_loss=None, take_profit=None, order_type="MARKET"):
        if len(symbol) == 6:
            instr = f"{symbol[:3]}_{symbol[3:]}"
        else:
            instr = f"USD_{symbol}"
        order = {"order": {"type": "MARKET", "instrument": instr,
                           "units": str(int(units)), "timeInForce": "FOK"}}
        if stop_loss:
            order["order"]["stopLossOnFill"] = {"price": str(stop_loss)}
        if take_profit:
            order["order"]["takeProfitOnFill"] = {"price": str(take_profit)}
        resp = self.ctx.order.create(self.account_id, order)
        if resp.status != 201:
            raise Exception(f"Order failed: {resp.body}")
        return resp.body
    def get_open_positions(self):
        resp = self.ctx.position.list_open(self.account_id)
        return resp.body.get("positions", []) if resp.status == 200 else []
    def get_order_history(self):
        resp = self.ctx.order.list(self.account_id, {"count": 50})
        return resp.body.get("orders", []) if resp.status == 200 else []

@st.cache_resource
def get_trading_api():
    try:
        import v20
        oanda_api_key = os.getenv("OANDA_API_KEY") or st.secrets.get("OANDA_API_KEY")
        oanda_account_id = os.getenv("OANDA_ACCOUNT_ID") or st.secrets.get("OANDA_ACCOUNT_ID")
        if oanda_api_key and oanda_account_id:
            from v20 import Context
            ctx = Context(hostname="api-fxpractice.oanda.com", port=443, token=oanda_api_key)
            return OANDA_Trading(ctx, oanda_account_id)
    except ImportError:
        pass
    return SimulatedTrading(st.session_state.trading_account)
