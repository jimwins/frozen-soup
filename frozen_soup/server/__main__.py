import argparse
import sys

from .. import freeze_to_string

from http.server import BaseHTTPRequestHandler, HTTPServer
import socketserver

class FrozenSoupRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        url = self.path[1:] # trim leading /

        # TODO Some error handling would be nice
        content = freeze_to_string(url)

        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(bytes(content, 'utf-8'))

def main() -> int:
    parser = argparse.ArgumentParser(
        prog = 'server',
        description  = 'Serve up single-file HTML page for a URL',
    )
    parser.add_argument(
        '-H', '--host',
        type=str,
        default='localhost',
        help='default port'
    )
    parser.add_argument(
        '-p', '--port',
        type=int,
        default=8080,
        help='default port'
    )

    args = parser.parse_args()

    with socketserver.TCPServer((args.host, args.port), FrozenSoupRequestHandler) as httpd:
        print(f"Server started http://{args.host}:{args.port}")
        httpd.serve_forever()

    return 0

if __name__ == '__main__':
    sys.exit(main())
