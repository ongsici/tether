FROM python:3.10-slim

WORKDIR /flight-app

COPY requirements.txt .  

RUN pip install --no-cache-dir -r requirements.txt

COPY . .  

RUN chmod +x script/start.sh

EXPOSE 9000

CMD ["bash", "/flight-app/script/start.sh"]