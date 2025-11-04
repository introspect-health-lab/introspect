#!/bin/bash
echo "Starting Introspect in development mode..."
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
