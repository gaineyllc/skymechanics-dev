FROM python:3.12-slim

WORKDIR /app

COPY services/invoice-service/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY services/invoice-service/ .
COPY shared /app/shared

EXPOSE 8207

CMD ["/bin/bash", "-c", "uvicorn main:app --host 0.0.0.0 --port ${PORT:-8207}"]
