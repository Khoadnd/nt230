import http.server
import socketserver


Handler = http.server.SimpleHTTPRequestHandler

Handler.extensions_map[".gif"] = "application/octet-stream"
Handler.extensions_map[".jpg"] = "application/octet-stream"
httpd = socketserver.TCPServer(("", 0), Handler)

# get port
PORT = httpd.socket.getsockname()[1]
print("Serving at http://localhost:{}".format(PORT))

while True:
    httpd.handle_request()
