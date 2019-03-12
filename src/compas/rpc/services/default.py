"""This script starts a XMLRPC server and registers the default service.

The server address is *localhost* and it listens to requests on port *1753*

"""

from compas.rpc import Server
from compas.rpc import Dispatcher


class DefaultService(Dispatcher):
    pass


# ==============================================================================
# main
# ==============================================================================

if __name__ == '__main__':

    import sys

    try:
        port = int(sys.argv[3])
    except:
        port = 1753

    print('Starting default RPC service on port {0}...'.format(port))

    # start the server on *localhost*
    # and listen to requests on port *1753*
    server = Server(("localhost", port))

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
