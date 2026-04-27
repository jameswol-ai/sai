# run_bot.py
"""
Standalone runner for the SAI trading bot.
Executes run_bot() from sai.bot.main.
"""

from sai.bot.main import run_bot

if __name__ == "__main__":
    print("Starting SAI trading bot...")
    run_bot()
