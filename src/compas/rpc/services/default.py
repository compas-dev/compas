"""This script starts a XMLRPC server and registers the default service.

The server binds to all network interfaces (i.e. ``0.0.0.0``) and
it listens to requests on port ``1753``.

"""
import os
import sys

from watchdog.events import PatternMatchingEventHandler
from watchdog.observers import Observer

from compas.rpc import Dispatcher
from compas.rpc import Server


class DefaultService(Dispatcher):

    def __init__(self):
        super(DefaultService, self).__init__()


class FileWatcherService(Dispatcher):
    def __init__(self):
        super(FileWatcherService, self).__init__()
        self.current_module = None
        self.current_observer = None

    def on_module_imported(self, module, newly_loaded_modules):
        module_spec = module.__spec__
        module_dir = os.path.dirname(module_spec.origin)

        # Stop existing observer, if any
        if self.current_module != module and self.current_observer:
            self.current_observer.stop()

        self.current_module = module
        reload_event_handler = ModuleReloader(newly_loaded_modules)

        print('Watching on {}'.format(module_dir))
        self.current_observer = Observer()
        self.current_observer.schedule(reload_event_handler, module_dir, recursive=True)
        self.current_observer.start()


class ModuleReloader(PatternMatchingEventHandler):
    def __init__(self, module_names):
        super(ModuleReloader, self).__init__(ignore_patterns=['__pycache__'])
        self.module_names = module_names

    def on_any_event(self, event):
        if event.src_path.endswith('.py'):
            # Unload modules so that they are reloaded on the next invocation
            for module in self.module_names:
                if module in sys.modules:
                    sys.modules.pop(module)


def start_service(port, autoreload, **kwargs):
    print('Starting default RPC service on port {0}...'.format(port))

    # start the server on *localhost*
    # and listen to requests on port *1753*
    server = Server(("0.0.0.0", port))

    # register a few utility functions
    server.register_function(server.ping)
    server.register_function(server.remote_shutdown)

    # register an instance of the default service
    # the default service extends the base service
    # which implements a dispatcher protocol
    # the dispatcher will intercept any calls to functionality of the service
    # and redirect either to an explicitly defined method of the service
    # or to a function that is available on the PYTHONPATH
    service = DefaultService() if not autoreload else FileWatcherService()
    server.register_instance(service)

    print('Listening{}...'.format(' with autoreload of modules enabled' if autoreload else ''))
    print('Press CTRL+C to abort')
    server.serve_forever()


# ==============================================================================
# main
# ==============================================================================

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('--port', '-p', action='store', default=1753, type=int, help='RPC port number')
    parser.add_argument('--autoreload', dest='autoreload', action='store_true', help='Autoreload modules')
    parser.add_argument('--no-autoreload', dest='autoreload', action='store_false', help='Do not autoreload modules')
    parser.set_defaults(autoreload=True, func=start_service)

    args = parser.parse_args()
    if hasattr(args, 'func'):
        args.func(**vars(args))
    else:
        parser.print_help()
