import os
import inspect
import json
import socket

import compas

from compas.rpc import Server
from compas.rpc import Service
from compas.rpc import kill
from compas.rpc import ping


class DefaultService(Service):
    pass


if __name__ == '__main__':

    import sys

    try:
        port = int(sys.argv[1])
    except:
        port = 8118

    print('Starting default RPC service on port {0}...'.format(port))

    server = Server(("localhost", port))

    server.register_function(ping)
    server.register_function(kill)

    server.register_instance(DefaultService())

    print('Listening, press CTRL+C to abort...')
    server.serve_forever()
