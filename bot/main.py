# sai/bot/main.py
"""
Core trading bot logic for SAI.
Provides run_bot() entry point with mode and config support.
"""

import logging
import time
import random

# Example simple model class
class SimpleModel:
    def predict(self, data):
        # Dummy prediction logic
        return random.choice(["BUY", "SELL", "HOLD"])

def setup_logger():
    logger = logging.getLogger("SAI_Bot")
    logger.setLevel(logging.INFO)
    fh = logging.FileHandler("sai_bot.log")
    fh.setLevel(logging.INFO)
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    return logger

def get_data():
    # Replace with real market data fetch
    return {"price": random.uniform(90, 110)}

def decide_action(model, data):
    return model.predict(data)

def execute_trade(action, mode, logger):
    if mode == "sandbox":
        logger.info(f"[SANDBOX] Simulated trade: {action}")
    elif mode == "live":
        logger.info(f"[LIVE] Executed trade: {action}")
    else:
        logger.info(f"[DEFAULT] Action: {action}")

def run_bot(mode="sandbox", config=None):
    logger = setup_logger()
    model = SimpleModel()

    logger.info("Starting SAI Bot...")
    logger.info(f"Mode: {mode}")
    if config:
        logger.info(f"Config loaded: {config}")

    try:
        while True:
            data = get_data()
            action = decide_action(model, data)
            execute_trade(action, mode, logger)
            time.sleep(2)  # loop delay
    except KeyboardInterrupt:
        logger.info("Bot stopped by user.")
