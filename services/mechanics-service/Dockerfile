FROM python:3.12-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy shared models first for better caching
COPY shared/ /app/shared/

# Copy requirements
COPY services/mechanics-service/requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY services/mechanics-service/*.py .

# Create non-root user for security
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# Expose port
EXPOSE 8201

# Environment variables
ENV PORT=8201
ENV PYTHONUNBUFFERED=1
ENV FALKORDB_HOST=falkordb
ENV FALKORDB_PORT=6379

# Run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "${PORT}"]
