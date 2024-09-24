from http.server import HTTPServer, BaseHTTPRequestHandler

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

    def do_GET(self):
        if self.path == '/':
            self.path = '/status'
        try:
            if self.path == '/status': 
                self.htmlDoc = b'status page'
            self._set_headers()
            self.wfile.write(self.htmlDoc)
        except:
            self.send_response(404)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b'404 - Not Found')


httpd = HTTPServer(('', 8000), SimpleHTTPRequestHandler)
httpd.serve_forever()