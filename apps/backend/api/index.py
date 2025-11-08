"""
Vercel serverless function entry point for FastAPI application.
This file is used by Vercel to handle all requests.

Vercel's @vercel/python runtime automatically detects FastAPI apps
and handles ASGI routing. The app variable is automatically used as the handler.
"""
from app.main import app

# Vercel will use 'app' as the ASGI handler
# No need to explicitly export - Vercel detects FastAPI automatically

