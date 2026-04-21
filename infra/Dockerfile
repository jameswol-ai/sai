# infra/Dockerfile
# Base image: lightweight Python
FROM python:3.11-slim

# Set working directory inside container
WORKDIR /app

# Install system dependencies (if needed for indicators, ML libs, etc.)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy dependency list first for caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Environment variables (can be overridden at runtime)
ENV PYTHONUNBUFFERED=1
ENV ENV_FILE=.env

# Entrypoint: run trading bot
ENTRYPOINT ["python", "bot/main.py"]
