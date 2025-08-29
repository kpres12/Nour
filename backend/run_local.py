#!/usr/bin/env python3
"""
Simple local development server for Nour
This script creates the database tables and starts the FastAPI server
"""

import os
import sys
from pathlib import Path

# Add the current directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

from app.core.db import engine, Base
from app.core.models import *  # Import all models
from app.main import app
import uvicorn

def setup_database():
    """Create database tables"""
    print("🗄️  Setting up local database...")
    try:
        # Create all tables
        Base.metadata.create_all(bind=engine)
        print("✅ Database tables created successfully")
    except Exception as e:
        print(f"⚠️  Database setup warning: {e}")
        print("Continuing with server startup...")

def main():
    """Main function to start the server"""
    print("🚀 Starting Nour local development server...")
    
    # Setup database
    setup_database()
    
    # Start server
    print("🌐 Starting FastAPI server on http://localhost:8000")
    print("📚 API documentation available at http://localhost:8000/docs")
    print("🔑 Use any email/password to login (demo mode)")
    print("")
    print("Press Ctrl+C to stop the server")
    
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )

if __name__ == "__main__":
    main()
