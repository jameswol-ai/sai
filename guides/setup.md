# Setup Guide

This document explains how to set up the AI Trading Bot environment, install dependencies, and configure the system for development and production.

---

## 1. Repository Structure
`
ai-trading-bot/
│
├── bot/                # Core trading logic
├── models/             # ML models (e.g., model.pkl)
├── guides/             # Documentation (setup, strategies, risk, deployment)
├── tests/              # Unit and integration tests
├── requirements.txt    # Python dependencies
├── Dockerfile          # Containerization
└── README.md           # Project overview
`

---

## 2. Prerequisites

- **Python 3.9+**
- **pip** (Python package manager)
- **Docker** (optional, for containerized deployment)
- **Git** (for version control)
- Broker API credentials (e.g., Alpaca, Interactive Brokers)

---

## 3. Installation

Clone the repository:

```bash
git clone https://github.com/your-username/ai-trading-bot.git
cd ai-trading-bot

pip install -r requirements.txt

BROKER_API_KEY=your_api_key
BROKER_SECRET=your_secret
BROKER_ENDPOINT=https://paper-api.alpaca.markets

from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("BROKER_API_KEY")

python trading_bot.py

docker build -t ai-trading-bot .
docker run --env-file .env ai-trading-bot
