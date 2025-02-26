#!/bin/bash

# exit on any error
set -e

HOST="0.0.0.0"
PORT="9000"

exec uvicorn app:app --host $HOST --port $PORT