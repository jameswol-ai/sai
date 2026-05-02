# --- Base image ---
FROM python:3.11-slim

# --- Set working directory ---
WORKDIR /app

# --- Copy repo files ---
COPY . /app

# --- Install dependencies ---
RUN pip install --no-cache-dir -r requirements.txt

# --- Expose Streamlit port ---
EXPOSE 8501

# --- Default command ---
CMD ["streamlit", "run", "sai/streamlit_app.py", "--server.port=8501", "--server.address=0.0.0.0"]
