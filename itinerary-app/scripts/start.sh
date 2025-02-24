#!/bin/bash

# exit on any error
set -e

cd /itinerary-app

HOST="0.0.0.0"
PORT="8000"

exec uvicorn app:app --host $HOST --port $PORT