import json
import importlib
import threading
import time

from compas.utilities import DataDecoder
from compas.utilities import DataEncoder

try:
    from http.server import BaseHTTPRequestHandler
except ImportError:
    from BaseHTTPServer import BaseHTTPRequestHandler


__all__ = ['RequestHandler']


class RequestHandler(BaseHTTPRequestHandler):

    def ping(self):
        return 1

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

        except Exception as e:
            odata['error'] = str(e)

        finally:
            response = json.dumps(odata, cls=DataEncoder).encode('utf-8')
            self.send_response(200)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.send_header('Content-Length', len(response))
            self.end_headers()
            self.wfile.write(response)


if __name__ == '__main__':

    pass
