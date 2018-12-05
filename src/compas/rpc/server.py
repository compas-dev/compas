from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

try:
    from SimpleXMLRPCServer import SimpleXMLRPCServer
except ImportError:
    from xmlrpc.server import SimpleXMLRPCServer


__all__ = ['Server', 'kill', 'ping']


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
    
    def serve_forever(self):
        while not self.quit:
            self.handle_request()


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


# def list_methods_wrapper(dispatcher):
#     def list_methods():
#         def is_public_method(member):
#             return inspect.ismethod(member) and not member.__name__.startswith('_')
#         members = inspect.getmembers(dispatcher, is_public_method)
#         return [member[0] for member in members]
#     return list_methods


# def method_help_wrapper(dispatcher):
#     def method_help(name):
#         if not hasattr(dispatcher, name):
#             return 'Not a registered API method: {0}'.format(name)
#         method = getattr(dispatcher, name)
#         return inspect.getdoc(method)
#     return method_help


# def method_signature_wrapper(dispatcher):
#     def method_signature(name):
#         if not hasattr(dispatcher, name):
#             return 'Not a registered API method: {0}'.format(name)
#         method = getattr(dispatcher, name)
#         spec = inspect.getargspec(method)
#         args = spec.args
#         defaults = spec.defaults
#         return args[1:], defaults
#     return method_signature


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":
    pass
