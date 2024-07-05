from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import threading

try:
    from SimpleXMLRPCServer import SimpleXMLRPCServer
except ImportError:
    from xmlrpc.server import SimpleXMLRPCServer


class Server(SimpleXMLRPCServer):
    """Version of a `SimpleXMLRPCServer` that can be cleanly terminated from the client side.

    Notes
    -----
    This class has to be used by a service to start the XMLRPC server in a way
    that can be pinged to check if the server is alive, and can be cleanly terminated.

    Examples
    --------
    .. code-block:: python

        # service.py

        from compas.rpc import Server
        from compas.rpc import Dispatcher


        class DefaultService(Dispatcher):
            pass


        if __name__ == "__main__":
            server = Server(("localhost", 8888))

            server.register_function(server.ping)
            server.register_function(server.remote_shutdown)
            server.register_instance(DefaultService())
            server.serve_forever()

    """

    def __init__(self, address, *args, **kwargs):
        super(Server, self).__init__(address, *args, **kwargs)
        self.register_function(self.ping)
        self.register_function(self.remote_shutdown)

    def ping(self):
        """Simple function used to check if a remote server can be reached.

        Returns
        -------
        int
            Always returns 1, since the ping is considered a success
            if the function can be reached from the client.

        Notes
        -----
        Should be used together with an instance of `compas.rpc.Server`.

        """
        return 1

    def remote_shutdown(self):
        """Stop the server through a call from the client side.

        Returns
        -------
        int
            Always returns 1.

        """
        threading.Thread(target=self._shutdown_thread).start()
        return 1

    def _shutdown_thread(self):
        self.shutdown()
