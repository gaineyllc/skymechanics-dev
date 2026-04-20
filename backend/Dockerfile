FROM python:3.12-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Create app user
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# Copy application code
COPY main.py .
COPY db.py .
COPY models.py .
COPY settings.py .
COPY onboarding.py .
COPY routes/ ./routes/

# Create __init__.py if not present
RUN touch routes/__init__.py 2>/dev/null || true

# Expose port
EXPOSE 8000

# Default port (can be overridden via PORT env var)
ENV PORT=8000

# Run application
CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port ${PORT} --reload"]
