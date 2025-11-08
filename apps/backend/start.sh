#!/bin/bash
# Start script for the FastAPI backend
# This script can be used for local development and is compatible with Vercel deployment

# Load environment variables from .env if it exists
if [ -f .env ]; then
    export $(cat .env | grep -v '^#' | xargs)
fi

# Set default port if not set
export PORT=${PORT:-8000}

# Start the server using uv run to ensure we use the virtual environment
# For Vercel, PORT is automatically set
# For local development, default to 8000
exec uv run python -m app

