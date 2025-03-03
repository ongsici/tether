#!/bin/bash

# exit on any error
set -e

HOST="0.0.0.0"
PORT="8080"

exec uvicorn src.app:app --host $HOST --port $PORT