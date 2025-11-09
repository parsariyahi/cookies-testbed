import http.server
import socketserver

class CookieHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        path = self.path
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        
        if path == '/':
            self.send_header('Set-Cookie', 'samesite_none=value; SameSite=None; Secure')
            self.send_header('Set-Cookie', 'samesite_lax=value; SameSite=Lax')
            self.send_header('Set-Cookie', 'samesite_strict=value; SameSite=Strict')
            self.send_header('Set-Cookie', 'samesite_default=value')
            self.send_header('Set-Cookie', 'samesite_default_secure=value; Secure;')
            self.send_header('Set-Cookie', 'secure_httponly=value; Secure; HttpOnly')
            self.send_header('Set-Cookie', 'no_flags=value')
            self.end_headers()
            self.wfile.write(b'<html><body>Cookies set. Visit <a href="/read_cookies">/read_cookies</a> to view.</body></html>')
        elif path == '/read_cookies':
            cookies = self.headers.get('Cookie', 'No cookies received')
            body = f'<html><body>Received cookies: {cookies}</body></html>'.encode('utf-8')
            self.send_header('Content-Length', str(len(body)))
            self.end_headers()
            self.wfile.write(body)
        else:
            self.end_headers()
            self.wfile.write(b'<html><body>Visit <a href="/">/</a> to set cookies.</body></html>')

    def do_POST(self):
        self.do_GET()

with socketserver.TCPServer(("", 8000), CookieHandler) as httpd:
    print("Serving at port 8000")
    httpd.serve_forever()