import http.server
import socketserver

class ClientHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            html = '''
<html><body>
<h1>Test Cross-Site Requests to http://localhost:8000/read_cookies</h1>
<p>First, visit http://localhost:8000/set_cookies to set cookies.</p>
<h2>HTML Form GET (top-level cross-site GET)</h2>
<form action="http://localhost:8000/read_cookies" method="GET">
<input type="submit" value="Send Form GET">
</form>
<h2>HTML Form POST (top-level cross-site POST)</h2>
<form action="http://localhost:8000/read_cookies" method="POST">
<input type="submit" value="Send Form POST">
</form>
<h2>JS GET (cross-site subresource GET)</h2>
<button id="js-get">Send JS GET</button>
<div id="result-get"></div>
<h2>JS POST (cross-site subresource POST)</h2>
<button id="js-post">Send JS POST</button>
<div id="result-post"></div>
<script>
document.getElementById('js-get').addEventListener('click', function() {
    fetch('http://localhost:8000/read_cookies', {
        method: 'GET',
        credentials: 'include'
    }).then(response => response.text()).then(data => {
        document.getElementById('result-get').innerHTML = data;
    }).catch(error => {
        document.getElementById('result-get').innerHTML = 'Error: ' + error.message;
    });
});
document.getElementById('js-post').addEventListener('click', function() {
    fetch('http://localhost:8000/read_cookies', {
        method: 'POST',
        credentials: 'include'
    }).then(response => response.text()).then(data => {
        document.getElementById('result-post').innerHTML = data;
    }).catch(error => {
        document.getElementById('result-post').innerHTML = 'Error: ' + error.message;
    });
});
</script>
</body></html>
            '''
            self.wfile.write(html.encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()

with socketserver.TCPServer(("127.0.0.1", 8001), ClientHandler) as httpd:
    print("Serving at http://127.0.0.1:8001 for cross-site testing with localhost:8000")
    httpd.serve_forever()