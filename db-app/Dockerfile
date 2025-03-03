FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
# COPY . ./app

RUN apt-get update && apt-get install -y libpq-dev gcc
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ ./src
COPY scripts/start.sh ./start.sh

RUN chmod +x start.sh

EXPOSE 8080

# CMD ["bash", "./scripts/start.sh"]
CMD ["bash", "start.sh"]