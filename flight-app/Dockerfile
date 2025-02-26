FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY src/ ./src
COPY script/start.sh ./start.sh

RUN chmod +x start.sh

EXPOSE 9000

CMD ["bash", "start.sh"]