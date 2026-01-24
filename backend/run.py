#!/usr/bin/env python
"""
Backend Server Launcher

Starts the FastAPI backend server for Smart Building Energy Prediction.

Usage:
    python run.py              # Run on default port 8000
    python run.py --port 8001  # Run on custom port
    python run.py --host 127.0.0.1  # Bind to specific host
"""

import sys
import argparse
from pathlib import Path

# Add backend app to path
backend_path = Path(__file__).parent / "app"
sys.path.insert(0, str(backend_path.parent))

from app.main import app
import uvicorn


def main():
    """Parse arguments and start the server."""
    parser = argparse.ArgumentParser(
        description="Start the Smart Building Energy Prediction FastAPI backend"
    )
    parser.add_argument(
        "--host",
        default="0.0.0.0",
        help="Host to bind to (default: 0.0.0.0)"
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8000,
        help="Port to bind to (default: 8000)"
    )
    parser.add_argument(
        "--reload",
        action="store_true",
        default=False,
        help="Enable auto-reload on code changes (development only)"
    )
    parser.add_argument(
        "--workers",
        type=int,
        default=1,
        help="Number of worker processes (default: 1)"
    )
    
    args = parser.parse_args()
    
    print("\n" + "="*70)
    print("SMART BUILDING ENERGY PREDICTION - BACKEND")
    print("="*70)
    print(f"\n✓ Starting FastAPI server...")
    print(f"  - Host: {args.host}")
    print(f"  - Port: {args.port}")
    print(f"  - Reload: {args.reload}")
    print(f"  - Workers: {args.workers}")
    print(f"\n📚 API Documentation:")
    print(f"  - Swagger UI: http://{args.host if args.host != '0.0.0.0' else 'localhost'}:{args.port}/docs")
    print(f"  - ReDoc: http://{args.host if args.host != '0.0.0.0' else 'localhost'}:{args.port}/redoc")
    print(f"\nPress CTRL+C to stop the server\n")
    print("="*70 + "\n")
    
    # Start the server
    uvicorn.run(
        "app.main:app",
        host=args.host,
        port=args.port,
        reload=args.reload,
        workers=args.workers,
        log_level="info"
    )


if __name__ == "__main__":
    main()
