"""
Vercel Serverless Entry Point for FastAPI backend.
Vercel routes /api/* requests to this file.
"""
import sys
import os

# Add the backend directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from app.main import app  # noqa: F401 - Vercel needs this imported
