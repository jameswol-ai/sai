# bot/main.py

from sai.utils import setup_logger

logger = setup_logger("sai_bot")

class SimpleModel:
    def predict(self, data):
        # Dummy prediction logic
        return "BUY" if sum(data) % 2 == 0 else "SELL"

def get_data():
    # Replace with real data ingestion
    return [1, 2, 3, 4]

def decide_action(data):
    model = SimpleModel()
    return model.predict(data)

def run_bot():
    data = get_data()
    action = decide_action(data)
    logger.info(f"Bot decided to: {action}")
    return action
