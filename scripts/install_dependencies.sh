#!/bin/bash
set -e

echo "[INSTALL] Installing Python dependencies on EC2"

cd /var/www/ai-test-analytics-hub

# Use the system pip, don't try to upgrade/uninstall it
python3 -m pip install -r requirements.txt
