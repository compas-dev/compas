"""This script starts a XMLRPC server and registers the default service.

The server binds to all network interfaces (i.e. ``0.0.0.0``) and
it listens to requests on port ``1753``.

"""

from compas.rpc import Dispatcher
from compas.rpc import Server


class DefaultService(Dispatcher):

    def __init__(self):
        super(DefaultService, self).__init__()


def start_service(port):
    print('Starting default RPC service on port {0}...'.format(port))

    # start the server on *localhost*
    # and listen to requests on port *1753*
    server = Server(("0.0.0.0", port))

    # register a few utility functions
    server.register_function(server.ping)
    server.register_function(server.remote_shutdown)

    # register an instance of the default service
    # the default service extends the base service
    # which implements a dispatcher protocol
    # the dispatcher will intercept any calls to functionality of the service
    # and redirect either to an explicitly defined method of the service
    # or to a function that is available on the PYTHONPATH
    server.register_instance(DefaultService())

    print('Listening, press CTRL+C to abort...')
    server.serve_forever()


# ==============================================================================
# main
# ==============================================================================

if __name__ == '__main__':
    import sys

    try:
        port = int(sys.argv[3])
    except Exception:
        port = 1753

    start_service(port)
