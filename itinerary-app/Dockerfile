FROM python:3.9-slim

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000
EXPOSE 11434

ENV OLLAMA_HOST="http://0.0.0.0:11434"

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]