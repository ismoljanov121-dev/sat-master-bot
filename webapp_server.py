"""
SAT AI Bot - WebApp Local Server (aiohttp with full /api/v1/ support)
Runs both the WebApp static files and the complete REST API on port 8080.
"""

import os
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

from aiohttp import web
from bot import setup_web_app
from config import PORT


def run_server(port=None):
    server_port = port or PORT or 8080
    app = setup_web_app()
    print(f"✅ WebApp and REST API server running on http://127.0.0.1:{server_port}")
    print(f"👉 Open http://127.0.0.1:{server_port}/webapp in your browser")
    web.run_app(app, host="0.0.0.0", port=server_port)


if __name__ == "__main__":
    run_server()
