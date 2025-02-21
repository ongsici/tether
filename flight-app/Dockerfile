FROM python:3.10-slim

RUN apt-get update \
    && apt-get install -y build-essential libpq-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .

RUN pip install -U pip && \
    pip install --no-cache-dir -r requirements.txt

COPY src /app/src

# Set environment variables (optional, can be handled securely with Docker secrets or .env files)
# ENV AMAD_CLIENT_ID="your_client_id"
# ENV AMAD_CLIENT_SECRET="your_client_secret"

WORKDIR /app/src

EXPOSE 8000

CMD ["uvicorn", "src.app:app", "--host", "0.0.0.0", "--port", "8000"]

