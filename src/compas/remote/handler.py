import json
import os
import importlib
import threading
import time
import traceback

from compas.utilities import DataDecoder
from compas.utilities import DataEncoder

try:
    from http.server import BaseHTTPRequestHandler
    from http.server import SimpleHTTPRequestHandler
except ImportError:
    from BaseHTTPServer import BaseHTTPRequestHandler
    from SimpleHTTPServer import SimpleHTTPRequestHandler


HERE = os.path.realpath(os.path.dirname(__file__))


__all__ = ['RequestHandler']


class RequestHandler(SimpleHTTPRequestHandler):

    def ping(self):
        return 1

    # def do_GET(self):
    #     self.send_response(200)
    #     self.send_header('Content-type', 'text/html')
    #     self.send_header('Content-Length', os.path.getsize(self.getPath()))
    #     self.end_headers()
    #     self.wfile.write(self.getContent(self.getPath()))

    # def getPath(self):
    #     if self.path == '/':
    #         content_path = os.path.join(HERE, 'index.html')
    #     else:
    #         content_path = os.path.join(HERE, str(self.path))
    #     return content_path

    # def getContent(self, content_path):
    #     with open(content_path, mode='r', encoding='utf-8') as f:
    #         content = f.read()
    #     return bytes(content, 'utf-8')

    def do_POST(self):
        odata = {}
        odata['data'] = None
        odata['error'] = None
        odata['profile'] = None

        try:
            itype = self.headers.get('Content-Type')
            ilength = self.headers.get('Content-Length')
            ilength = int(ilength)
            ibody = self.rfile.read(ilength).decode('utf-8')
            idata = json.loads(ibody, cls=DataDecoder)

            modulename = idata['module']
            functionname = idata['function']
            args = idata.get('args') or []
            kwargs = idata.get('kwargs') or {}

            if not modulename:
                module = self
            else:
                module = importlib.import_module(modulename)

            function = getattr(module, functionname)

            result = function(*args, **kwargs)
            odata['data'] = result

        except:
            odata['error'] = traceback.format_exc()

        finally:
            response = json.dumps(odata, cls=DataEncoder).encode('utf-8')
            self.send_response(200)
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.send_header('Content-Length', len(response))
            self.end_headers()
            self.wfile.write(response)


if __name__ == '__main__':

    pass
