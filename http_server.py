import http.server
import socketserver
import logging


class CustomHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # Always serve the same file, ignoring the actual request path
        self.path = "./assets/test_pattern.png"
        logging.info(f"Received request, serving file: {self.path}")
        try:
            with open(self.path, 'rb') as f:
                self.send_response(200)
                self.send_header('Content-type', 'image/png')
                self.end_headers()
                self.copyfile(f, self.wfile)
        except BrokenPipeError:
            logging.debug("Client terminated the connection before the response was complete.")


def start_http_server(port=80):
    Handler = CustomHTTPRequestHandler
    httpd = socketserver.TCPServer(("", port), Handler)
    print(f"Serving at port {port}")
    return httpd


