#!/bin/bash
# Rebuild container and restart bore tunnel

set -e

cd ~/Desktop/reading-assistant/.devcontainer

echo "==> Stopping bore..."
pkill -f "bore local" || true

echo "==> Rebuilding container..."
docker compose down
docker compose up -d --build

echo "==> Waiting for SSH to be ready..."
sleep 10

echo "==> Starting bore tunnel..."
bore local 2222 --to bore.pub > /tmp/bore.log 2>&1 &
sleep 3

# Extract port from bore output
PORT=$(grep -o 'bore.pub:[0-9]*' /tmp/bore.log | head -1 | cut -d: -f2)

if [ -z "$PORT" ]; then
    echo "ERROR: Could not detect bore port. Check /tmp/bore.log"
    cat /tmp/bore.log
    exit 1
fi

echo "==> Installing SSH key..."
ssh-copy-id -i ~/.ssh/reading_assistant -p $PORT root@bore.pub

echo ""
echo "=========================================="
echo "Bore port for solveit: $PORT"
echo "=========================================="
