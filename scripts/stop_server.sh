#!/bin/bash
set -e

echo "[STOP] Stopping existing FastAPI service if running"

# If you later create a systemd service, use:
# systemctl stop ai-test-analytics-hub || true

# For now, just kill uvicorn processes (simple dev setup)
pkill -f "uvicorn" || echo "No uvicorn process found"
