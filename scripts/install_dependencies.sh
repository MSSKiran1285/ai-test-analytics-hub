#!/bin/bash
set -e

echo "[INSTALL] Installing Python dependencies on EC2"

cd /var/www/ai-test-analytics-hub

# Use a virtualenv if you prefer; for test deployment we keep it simple.
python3 -m pip install --upgrade pip
pip3 install -r requirements.txt
