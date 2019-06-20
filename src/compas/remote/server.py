import threading
from http.server import HTTPServer
from handler import RequestHandler


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


if __name__ == '__main__':

    server = ThreadedServer()
    server.start()
