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

    import threading

    server = Server(("localhost", 1753))

    server.register_function(server.ping)
    server.register_function(server.remote_shutdown)

    server.register_instance(DefaultService())

    server.serve_forever()
