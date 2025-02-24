FROM python:3.10-slim
 
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . /itinerary-app

RUN chmod +x itinerary-app/scripts/start.sh

EXPOSE 8000

CMD ["bash", "/itinerary-app/scripts/start.sh"]
