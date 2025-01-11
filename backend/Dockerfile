FROM python:3.9-slim

WORKDIR /app

# Install system dependencies including netcat-openbsd
RUN apt-get update && apt-get install -y \
    postgresql-client \
    netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Make the script executable
RUN chmod +x scripts/seed_database.py

# Default command yang akan di-override oleh docker-compose
CMD uvicorn main:app --host 0.0.0.0 --port 8000