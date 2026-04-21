FROM python:3.12-slim

WORKDIR /app

COPY services/parts-service/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY services/parts-service/ .
COPY shared /app/shared

EXPOSE 8201

CMD ["/bin/bash", "-c", "uvicorn main:app --host 0.0.0.0 --port ${PORT:-8201}"]
