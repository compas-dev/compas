import os
import inspect
import json
import socket

import compas

from compas.rpc import Server
from compas.rpc import Service
from compas.rpc import kill
from compas.rpc import ping
from compas.rpc import shutdown


class DefaultService(Service):
    pass


if __name__ == '__main__':

    server = Server(("localhost", 8888))

    server.register_function(ping)
    server.register_function(shutdown)

    server.register_instance(DefaultService())

    server.serve_forever()
