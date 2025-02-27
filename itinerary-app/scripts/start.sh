#!/bin/bash

# exit on any error
set -e

cd /itinerary-app

HOST="0.0.0.0"
PORT="7000"

exec uvicorn app:app --host $HOST --port $PORT