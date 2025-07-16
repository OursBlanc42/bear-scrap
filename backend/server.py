#!/usr/bin/env python3
"""
Simple HTTP server to serve the web application for local testing.
"""

import http.server
import socketserver
import os
import sys


def main():
    port = 8000
    os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

    handler = http.server.SimpleHTTPRequestHandler

    try:
        with socketserver.TCPServer(("", port), handler) as httpd:
            print(f"Serveur démarré sur http://localhost:{port}")
            print(f"Access http://localhost:{port}/web/ to view the site")
            print("Press Ctrl+C to stop the server")
            httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")
        sys.exit(0)


if __name__ == "__main__":
    main()
