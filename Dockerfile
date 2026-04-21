# Dockerfile for SAI Trading Bot

# Use official Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy repo files
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Default command: run main.py
ENTRYPOINT ["python", "bot/main.py"]
