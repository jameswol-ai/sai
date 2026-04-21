import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

BROKER_API_KEY = os.getenv("BROKER_API_KEY")
BROKER_SECRET = os.getenv("BROKER_SECRET")
BROKER_ENDPOINT = os.getenv("BROKER_ENDPOINT")

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
