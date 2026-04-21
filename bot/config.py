import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

API_KEY = os.getenv("API_KEY")
DATA_SOURCE_URL = os.getenv("DATA_SOURCE_URL")
TRADING_MODE = os.getenv("TRADING_MODE", "paper")  # default to paper trading
