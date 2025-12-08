#!/bin/bash
set -e

echo "[START] Starting FastAPI with uvicorn"

cd /var/www/ai-test-analytics-hub

# Run as a background process on port 8000 (for test deployment)
nohup uvicorn app.main:app --host 0.0.0.0 --port 8000 > uvicorn.log 2>&1 &
