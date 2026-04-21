# SAI - AI Trading Bot

An intelligent algorithmic trading bot that uses machine learning to predict market movements and execute trades automatically.

## Features

- **Machine Learning Model**: Uses Random Forest classifier trained on OHLCV data
- **Multiple Trading Modes**: Train, Evaluate, Backtest, Deploy, and Live Trading
- **Exchange Integration**: Supports Binance and other exchanges via CCXT
- **Modular Architecture**: Clean separation of concerns with plugins and pipelines
- **Configuration Management**: JSON-based configuration for all components
- **Comprehensive Testing**: Full test suite with pytest

## Project Structure

```
sai/
├── bot/
│   ├── main.py           # Main entry point with CLI
│   ├── strategy.py       # ML strategy implementation
│   ├── trader.py         # Trading logic and execution
│   ├── data.py           # Data fetching utilities
│   └── utils.py          # Utility functions
├── models/
│   ├── train.py          # Model training script
│   ├── evaluate.py       # Model evaluation script
│   └── pipelines/        # ML pipelines
│       ├── train_pipeline.py
│       ├── evaluate_pipeline.py
│       ├── backtest_pipeline.py
│       └── deploy_pipeline.py
├── plugins/
│   ├── exchanges/        # Exchange integrations
│   ├── indicators/       # Technical indicators
│   └── broker.py         # Broker API wrapper
├── configs/              # Configuration files
├── scripts/              # Utility scripts
├── tests/                # Test suite
├── data/                 # Training/test data
├── logs/                 # Log files
├── infra/                # Infrastructure configs
└── requirements.txt      # Python dependencies
```

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Generate Sample Data

```bash
python scripts/generate_sample_data.py
```

### 3. Train the Model

```bash
python bot/main.py --mode train
```

### 4. Evaluate Performance

```bash
python bot/main.py --mode evaluate
```

### 5. Run Backtest

```bash
python bot/main.py --mode backtest
```

## Usage

### Command Line Interface

```bash
python bot/main.py --mode [train|evaluate|backtest|deploy|live] [--config CONFIG_FILE]
```

### Modes

- **train**: Train the ML model on historical data
- **evaluate**: Evaluate model performance on test data
- **backtest**: Simulate trading on historical data
- **deploy**: Deploy the model to production (Docker/K8s)
- **live**: Run live trading (requires API keys)

### Configuration

All modes use JSON configuration files in the `configs/` directory:

- `train_config.json`: Training parameters
- `evaluate_configs.json`: Evaluation parameters
- `backtest_config.json`: Backtesting parameters
- `deploy_config.json`: Deployment settings

## Environment Setup

Create a `.env` file with your API credentials:

```env
BROKER_API_KEY=your_api_key_here
BROKER_SECRET=your_secret_here
BROKER_ENDPOINT=https://paper-api.alpaca.markets
```

## Web API

The AI trading bot includes a REST API for real-time predictions:

```bash
# Start the API server
python api.py

# Health check
curl http://localhost:8000/health

# Get prediction
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"open": 50000, "high": 51000, "low": 49000, "close": 50500, "volume": 1000}'
```

**Response:**
```json
{
  "prediction": 0,
  "probability_class_0": 0.93,
  "probability_class_1": 0.07,
  "signal": "SELL"
}
```

## Deployment

### Docker

```bash
docker build -t sai-trading-bot .
docker run sai-trading-bot
```

### Kubernetes

```bash
kubectl apply -f k8s/deployment.yaml
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all tests pass
5. Submit a pull request

## License

See LICENSE file for details.

## Disclaimer

This software is for educational purposes only. Trading cryptocurrencies involves significant risk. Use at your own risk.

sai/
├── bot/                     # Core trading bot logic
│   ├── main.py              # Entry point
│   ├── data.py              # Data ingestion & preprocessing
│   ├── strategy.py          # Strategy definitions
│   ├── risk.py              # Risk management rules
│   ├── trader.py            # Trade execution engine
│   └── utils.py             # Shared utilities

├── models/                  # ML models
│   ├── train.py             # Training scripts
│   ├── evaluate.py          # Model evaluation
│   ├── model.pkl            # Serialized model
│   └── pipelines/           # Modular ML pipelines

├── plugins/                 # Optional extensions
│   ├── indicators/          # Technical indicators
│   ├── exchanges/           # Exchange API connectors
│   └── notifications/       # Alerts (Slack, email, etc.)

├── guides/                  # Documentation guides
│   ├── setup.md
│   ├── strategies.md
│   ├── risk.md
│   ├── workflow.md
│   └── deployment.md

├── tests/                   # Testing suite
│   ├── unit/                # Unit tests
│   ├── integration/         # End-to-end tests
│   └── conftest.py          # Pytest config

├── docs/                    # General documentation
│   ├── units.md             # Currency, conversions
│   ├── position_sizing.md
│   └── examples.md

├── infra/                   # Infrastructure & CI/CD
│   ├── Dockerfile
│   ├── docker-compose.yml
│   ├── requirements.txt
│   ├── .env.example
│   └── .github/
│       └── workflows/
│           └── ci-cd.yml    # GitHub Actions pipeline

├── scripts/                 # Utility scripts
│   ├── backtest.py          # Backtesting engine
│   ├── live_trading.py      # Live trading runner
│   └── data_fetch.py        # Data collection

├── README.md                # Project overview
└── LICENSE                  # License file

## Web API

The AI trading bot includes a REST API for real-time predictions:

```bash
# Start the API server
python api.py

# Health check
curl http://localhost:8000/health

# Get prediction
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"open": 50000, "high": 51000, "low": 49000, "close": 50500, "volume": 1000}'
```

**Response:**
```json
{
  "prediction": 0,
  "probability_class_0": 0.93,
  "probability_class_1": 0.07,
  "signal": "SELL"
}
```
