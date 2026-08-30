FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY . .

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Cloud Run injects the PORT environment variable. Defaults to 8000.
CMD exec uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}
