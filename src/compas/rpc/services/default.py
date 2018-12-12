import os
import inspect
import json
import socket

import compas

from compas.rpc import Server
from compas.rpc import Service


class DefaultService(Service):
    pass


if __name__ == '__main__':

    import sys
    import threading

    try:
        port = int(sys.argv[1])
    except:
        port = 1753

    print('Starting default RPC service on port {0}...'.format(port))

    server = Server(("localhost", port))

    server.register_function(server.ping)
    server.register_function(server.remote_shutdown)

    server.register_instance(DefaultService())

    print('Listening, press CTRL+C to abort...')
    server.serve_forever()
