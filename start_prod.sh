#!/bin/bash
echo "Starting Introspect in production mode..."
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
uvicorn src.main:app --host 0.0.0.0 --port 8000 --workers 4
