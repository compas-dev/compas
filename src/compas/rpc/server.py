from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import threading

try:
    from SimpleXMLRPCServer import SimpleXMLRPCServer
except ImportError:
    from xmlrpc.server import SimpleXMLRPCServer


__all__ = ['Server']


class Server(SimpleXMLRPCServer):
    """Version of a `SimpleXMLRPCServer` that can be ceanly terminated from the client side.

    Examples
    --------
    .. code-block:: python

        # service.py

        from compas.rpc import Server
        from compas.rpc import Dispatcher


        class DefaultService(Dispatcher):
            pass


        if __name__ == '__main__':

            server = Server(("localhost", 8888))

            server.register_function(server.ping)
            server.register_function(server.remote_shutdown)
            server.register_instance(DefaultService())
            server.serve_forever()

    Notes
    -----
    This class has to be used by a service to start the XMLRPC server in a way
    that can be pinged to check if the server is live, and can be cleanly terminated.

    """

    def ping(self):
        """Simple function used to check if a remote server can be reached.

        Notes
        -----
        Should be used together with an instance of `compas.rpc.Server`.

        """
        return 1

    def remote_shutdown(self):
        threading.Thread(target=self._shutdown_thread).start()
        return 1

    def _shutdown_thread(self):
        self.shutdown()


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":
    pass
