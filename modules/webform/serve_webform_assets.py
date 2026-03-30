"""
Lightweight static file server for the webform frontend assets.

Serves webform_bundle.js, custom.css, configs/, etc. on port 9000 so that
the engine's HTML shell (served on :8080) can load them via
<base href="http://…:9000/">.

Usage:
    python3 modules/webform/serve_webform_assets.py          # port 9000
    WEBFORM_PORT=3001 python3 modules/webform/serve_webform_assets.py
"""

import http.server
import os
import functools

PORT = int(os.environ.get("WEBFORM_PORT", 9000))
DIRECTORY = os.path.join(os.path.dirname(os.path.abspath(__file__)), "build", "dist")


class CORSHandler(http.server.SimpleHTTPRequestHandler):
    """SimpleHTTPRequestHandler with permissive CORS headers."""

    def end_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        super().end_headers()


def main():
    handler = functools.partial(CORSHandler, directory=DIRECTORY)
    with http.server.HTTPServer(("0.0.0.0", PORT), handler) as httpd:
        print(f"Serving webform assets from {DIRECTORY} on :{PORT}")
        httpd.serve_forever()


if __name__ == "__main__":
    main()
