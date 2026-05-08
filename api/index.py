"""
Vercel Serverless Entry Point for FastAPI backend.
Vercel routes /api/* requests to this file.
Uses Mangum to adapt FastAPI (ASGI) to serverless handler.
"""
import sys
import os

# Add the backend directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from mangum import Mangum
from app.main import app

# Mangum wraps FastAPI for serverless (AWS Lambda / Vercel)
handler = Mangum(app, lifespan="off")
