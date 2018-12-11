from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import socket
import threading

try:
    from SimpleXMLRPCServer import SimpleXMLRPCServer
except ImportError:
    from xmlrpc.server import SimpleXMLRPCServer


# socket.setdefaulttimeout(10)


__all__ = ['Server']


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

    # quit = False
    
    # def serve_forever(self):
    #     while not self.quit:
    #         self.handle_request()

    # def server_bind(self):
    #     self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    #     SimpleXMLRPCServer.server_bind(self)

    # def kill(self):
    #     """Helper function used to kill a remote sever.

    #     Notes
    #     -----
    #     Should be used together with an instance of `compas.rpc.Server`.

    #     """
    #     self.quit = True
    #     return 1


    def ping(self):
        """Simple function used to check if a remote server can be reached.

        Notes
        -----
        Should be used together with an instance of `compas.rpc.Server`.

        """
        return 1

    def remote_shutdown(self):
        threading.Thread(self._shutdown_thread).start()
        return 1

    def _shutdown_thread(self):
        self.shutdown()



# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":
    pass
