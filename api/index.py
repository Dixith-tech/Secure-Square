"""
Vercel Serverless Entry Point for FastAPI backend.
Routes: /api/* → this file → FastAPI app via Mangum (ASGI adapter).
"""
import sys
import os

# Add backend to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

# Set SQLite to /tmp for serverless (writable) when no DATABASE_URL is set
if not os.environ.get("DATABASE_URL"):
    os.environ["DATABASE_URL"] = "sqlite:////tmp/security_platform.db"

from mangum import Mangum
from app.main import app  # noqa: E402

# Mangum wraps the ASGI app for AWS Lambda / Vercel serverless
handler = Mangum(app, lifespan="off")
