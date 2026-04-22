FROM python:3.12-slim

WORKDIR /app

COPY services/auth-service/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY services/auth-service/ .

EXPOSE 8200

CMD ["/bin/bash", "-c", "uvicorn main:app --host 0.0.0.0 --port ${PORT:-8200} --log-level debug"]
