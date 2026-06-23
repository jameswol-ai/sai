import os
import csv
import pytest
from datetime import datetime
from sai.streamlit_app import Metrics, TradingBot, CSVExporter

@pytest.fixture
def bot():
    return TradingBot(currency="USD")

@pytest.fixture
def metrics():
    return Metrics()

@pytest.fixture
def csv_exporter(tmp_path):
    filename = tmp_path / "trades.csv"
    return CSVExporter(filename=str(filename))

def test_metrics_initialization(metrics):
    snap = metrics.snapshot(bot=TradingBot())
    assert snap["balance_usd"] == 1000
    assert snap["pnl_usd"] == 0
    assert snap["balance_local"] == 1000
    assert snap["pnl_local"] == 0

def test_metrics_update_and_snapshot(bot, metrics):
    fx_rates = {"USD": 1.0}
    price = bot.get_price()
    action, trade = bot.step(price)
    metrics.update(price, action, trade, bot, fx_rates)
    snap = metrics.snapshot(bot)
    assert snap["last_price"] == price
    assert snap["last_action"] == action
    assert isinstance(snap["balance_usd"], (int, float))

def test_csv_exporter_writes_and_reads(bot, metrics, csv_exporter):
    fx_rates = {"USD": 1.0}
    price = bot.get_price()
    action, trade = bot.step(price)
    metrics.update(price, action, trade, bot, fx_rates)
    snap = metrics.snapshot(bot)

    row = {
        "timestamp": datetime.utcnow().isoformat(),
        "price": price,
        "action": action,
        "trade": trade,
        "balance_usd": snap["balance_usd"],
        "balance_local": snap["balance_local"],
        "currency": snap["currency"],
        "pnl_usd": snap["pnl_usd"],
        "pnl_local": snap["pnl_local"],
    }
    csv_exporter.write_row(row)

    with open(csv_exporter.filename, "r", newline="") as f:
        reader = list(csv.reader(f))
        assert reader[0] == [
            "timestamp","price","action","trade",
            "balance_usd","balance_local","currency",
            "pnl_usd","pnl_local"
        ]
        assert len(reader) == 2  # header + one row
