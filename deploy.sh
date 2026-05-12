#!/bin/bash
set -e

echo "🚀 Deploying SAI Trading Bot..."

# 1. Environment setup
if [ ! -f ".env" ]; then
  echo "❌ Missing .env file with broker credentials"
  exit 1
fi

# 2. Build Docker image
docker build -t sai-bot .

# 3. Run container with metrics + logs
docker run -d \
  --env-file .env \
  -p 8501:8501 \   # Streamlit dashboard
  -p 8000:8000 \   # Prometheus metrics
  -v $(pwd)/trading.log:/app/trading.log \
  --name sai-live sai-bot

echo "✅ SAI bot running at http://localhost:8501"
echo "📊 Metrics available at http://localhost:8000"
