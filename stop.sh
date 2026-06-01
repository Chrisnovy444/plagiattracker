#!/bin/bash

# PLAGIATTRACKER - Stop Script

echo "🛑 Arrêt de PLAGIATTRACKER..."

# Stop backend
if [ -f backend.pid ]; then
    PID=$(cat backend.pid)
    echo "Arrêt backend (PID: $PID)..."
    kill $PID 2>/dev/null || true
    rm backend.pid
fi

# Stop frontend
if [ -f frontend.pid ]; then
    PID=$(cat frontend.pid)
    echo "Arrêt frontend (PID: $PID)..."
    kill $PID 2>/dev/null || true
    rm frontend.pid
fi

# Stop Docker containers
echo "Arrêt Docker containers..."
docker-compose down

echo "✅ PLAGIATTRACKER arrêté"
