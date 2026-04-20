FROM python:3.12-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY services/analytics-service/requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY services/analytics-service/*.py .

# Create non-root user for security
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# Expose port
EXPOSE 8203

# Environment variables
ENV PORT=8203
ENV PYTHONUNBUFFERED=1
ENV CLICKHOUSE_HOST=clickhouse
ENV CLICKHOUSE_PORT=9000

# Run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "${PORT}"]
