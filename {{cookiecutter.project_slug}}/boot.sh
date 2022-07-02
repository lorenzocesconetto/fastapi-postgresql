#!/bin/sh

if [[ $1 != 'production' && $RUN_JUPYTER_LAB == "true" ]]; then
    echo "Starting Jupyter Lab"
    jupyter lab --ip=0.0.0.0 --allow-root --NotebookApp.custom_display_url=http://127.0.0.1:8888 &
fi

if [[ $1 == 'debug' ]]; then
    echo "Running server in debug mode..."
    python -m debugpy --listen 0.0.0.0:5678 --wait-for-client app/main.py
elif [[ $1 == 'test' ]]; then
    echo "Running tests..."
    pytest tests
elif [[ $1 == 'development' ]]; then
    echo "Running server in development mode..."
    uvicorn app.main:app --host 0.0.0.0 --port 80 --reload
elif [[ $1 == 'production' ]]; then
    echo "Running server in production mode..."
    uvicorn app.main:app --host 0.0.0.0 --port 80
else
    echo "Must specify either 'debug', 'development', 'production' or 'test' as first argument."
    exit 1
fi
