"""This script starts a XMLRPC server and registers the default service.

The server binds to all network interfaces (i.e. ``0.0.0.0``) and
it listens to requests on port ``1753``.

"""

from compas.rpc import Dispatcher
from compas.rpc import Server

from .watcher import FileWatcherService


class DefaultService(Dispatcher):
    def __init__(self):
        super(DefaultService, self).__init__()

    def special(self):
        return "special"


def start_service(port=1753, autoreload=True, **kwargs):
    print("Starting default RPC service on port {0}...".format(port))

    # start the server on *localhost*
    # and listen to requests on port *1753*
    host = "0.0.0.0"
    address = host, port
    server = Server(address)

    # register an instance of the default service
    # the default service extends the base service
    # which implements a dispatcher protocol
    # the dispatcher will intercept any calls to functionality of the service
    # and redirect either to an explicitly defined method of the service
    # or to a function that is available on the PYTHONPATH
    service = DefaultService() if not autoreload else FileWatcherService()
    server.register_instance(service)

    print("Listening{}...".format(" with autoreload of modules enabled" if autoreload else ""))
    print("Press CTRL+C to abort")
    server.serve_forever()


# ==============================================================================
# main
# ==============================================================================

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--port",
        "-p",
        action="store",
        default=1753,
        type=int,
        help="RPC port number",
    )

    parser.add_argument(
        "--autoreload",
        dest="autoreload",
        action="store_true",
        help="Autoreload modules",
    )

    parser.add_argument(
        "--no-autoreload",
        dest="autoreload",
        action="store_false",
        help="Do not autoreload modules",
    )

    parser.set_defaults(
        autoreload=True,
        func=start_service,
    )

    args = parser.parse_args()

    if hasattr(args, "func"):
        args.func(**vars(args))
    else:
        parser.print_help()
