"""
SAT AI Bot - WebApp Local Static Server
Serves the 60-day interactive SAT Tracker on port 8080.
"""

import os
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

from http.server import HTTPServer, SimpleHTTPRequestHandler

WEBAPP_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "webapp")

class WebAppHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=WEBAPP_DIR, **kwargs)

    def end_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
        super().end_headers()

def run_server(port=8080):
    server = HTTPServer(("127.0.0.1", port), WebAppHandler)
    print(f"✅ WebApp static server running on http://127.0.0.1:{port}")
    server.serve_forever()

if __name__ == "__main__":
    run_server()
