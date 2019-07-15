import threading

try:
    from http.server import HTTPServer
except ImportError:
    from BaseHTTPServer import HTTPServer

from compas.remote import RequestHandler


__all__ = ['ThreadedServerError', 'ThreadedServer']


class ThreadedServerError(Exception):
    pass


class ThreadedServer(object):

    def __init__(self, host='0.0.0.0', port=1753, request_handler=RequestHandler):
        self.host = host
        self.port = port
        self.server = HTTPServer((self.host, self.port), request_handler)
        self.thread = threading.Thread(target=self.server.serve_forever)
        self.thread.daemon = False

    def start(self):
        self.thread.start()

    def stop(self):
        self.server.shutdown()
        self.server.server_close()


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':

    pass
