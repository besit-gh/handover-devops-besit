"""Small HTTP service used by the DevOps capstone project."""
import json
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer


def response_for(path: str) -> tuple[int, bytes, str]:
    """Return status, body and content type without opening a socket."""
    if path == "/health":
        body = {"status": "ok", "service": "demo-servicio"}
        return 200, json.dumps(body).encode("utf-8"), "application/json; charset=utf-8"
    if path == "/":
        body = {"service": "demo-servicio", "message": "Сервис работает"}
        return 200, json.dumps(body, ensure_ascii=False).encode("utf-8"), "application/json; charset=utf-8"
    return 404, json.dumps({"error": "not found"}).encode("utf-8"), "application/json; charset=utf-8"


class Handler(BaseHTTPRequestHandler):
    server_version = "DemoService/1.0"

    def do_GET(self) -> None:
        status, body, content_type = response_for(self.path)
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, fmt: str, *args: object) -> None:
        # Keep access logs concise and timestamped by the standard handler.
        print("%s - %s" % (self.log_date_time_string(), fmt % args), flush=True)


def main() -> None:
    host = os.environ.get("HOST", "0.0.0.0")
    port = int(os.environ.get("PORT", "8080"))
    server = ThreadingHTTPServer((host, port), Handler)
    print(f"starting demo-servicio on {host}:{port}", flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
