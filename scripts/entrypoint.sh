#!/bin/bash
# scripts/entrypoint.sh
# Entrypoint script for Docker to run migrations and start the app

set -e

echo "Running Alembic migrations..."
alembic upgrade head

echo "Seeding admin user..."
python scripts/seed_admin.py

echo "Starting Uvicorn server..."
uvicorn app.main:app --host 0.0.0.0 --port 8000
