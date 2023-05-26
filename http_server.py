import http.server
import socketserver
import logging


class CustomHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # Always serve the same file, ignoring the actual request path
        self.path = "/assets/test_pattern.png"
        logging.info(f"Received request, serving file: {self.path}")
        return http.server.SimpleHTTPRequestHandler.do_GET(self)


def start_http_server(port=80):
    Handler = CustomHTTPRequestHandler
    with socketserver.TCPServer(("", port), Handler) as httpd:
        print(f"Serving at port {port}")
        httpd.serve_forever()
