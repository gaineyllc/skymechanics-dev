FROM python:3.12-slim

WORKDIR /app

# Copy shared models first (needed before service code)
COPY shared /app/shared

COPY services/aircraft-service/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY services/aircraft-service/ .

EXPOSE 8205

CMD ["/bin/bash", "-c", "uvicorn main:app --host 0.0.0.0 --port ${PORT:-8205}"]
