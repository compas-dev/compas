from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

try:
    from SimpleXMLRPCServer import SimpleXMLRPCServer
except ImportError:
    from xmlrpc.server import SimpleXMLRPCServer

import threading


__all__ = ['Server', 'kill', 'ping', 'shutdown']


class Server(SimpleXMLRPCServer):
    """Version of a `SimpleXMLRPCServer` that can be ceanly terminated from the client side.

    Attributes
    ----------
    quit : bool
        Flag telling the server to stop handling requests.

    Examples
    --------
    .. code-block:: python

        # service.py

        from compas.rpc import Server
        from compas.rpc import Service
        from compas.rpc import kill
        from compas.rpc import ping


        class DefaultService(Service):
            pass


        if __name__ == '__main__':

            server = Server(("localhost", 8888))

            server.register_function(ping)
            server.register_function(kill)

            server.register_instance(DefaultService())

            server.serve_forever()

    """

    quit = False
    
    # def serve_forever(self):
    #     while True:
    #         if self.quit:
    #             break
    #         self.handle_request()


def kill():
    """Helper function used to kill a remote sever.

    Notes
    -----
    Should be used together with an instance of `compas.rpc.Server`.

    """
    Server.quit = True
    return 1


def ping():
    """Simple function used to check if a remote server can be reached.

    Notes
    -----
    Should be used together with an instance of `compas.rpc.Server`.

    """
    return 1


def shutdown():
    threading.Thread(shutdown_thread).start()
    return 1


def shutdown_thread():
    server.shutdown()


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":
    pass
