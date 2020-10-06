import time

from compas.rpc.services.default import start_service

try:
    from xmlrpclib import ServerProxy
except ImportError:
    from xmlrpc.client import ServerProxy


def start(port, autoreload, **kwargs):
    start_service(port, autoreload)


def stop(port, **kwargs):
    print('Trying to stop remote RPC proxy...')
    server = ServerProxy('http://127.0.0.1:{}'.format(port))

    success = False
    count = 5
    while count:
        try:
            server.ping()
        except Exception:
            time.sleep(0.1)
            count -= 1
            print("    {} attempts left.".format(count))
        else:
            success = True
            break

    if not success:
        print('RPC server did not respond. Maybe already stopped.')
    else:
        server.remote_shutdown()
        print('RPC server stopped')


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description='COMPAS RPC command-line utility')

    commands = parser.add_subparsers(help='Valid RPC commands')

    # Command: start
    start_command = commands.add_parser('start', help='Start RPC server')
    start_command.add_argument(
        '--port', '-p', action='store', default=1753, type=int, help='RPC port number')
    start_command.add_argument('--autoreload', dest='autoreload', action='store_true', help='Autoreload modules')
    start_command.add_argument('--no-autoreload', dest='autoreload', action='store_false', help='Do not autoreload modules')
    start_command.set_defaults(autoreload=True, func=start)

    # Command: stop
    stop_command = commands.add_parser(
        'stop', help='Try to stop a remote RPC server')
    stop_command.add_argument(
        '--port', '-p', action='store', default=1753, type=int, help='RPC port number')
    stop_command.set_defaults(func=stop)

    # Invoke
    args = parser.parse_args()
    if hasattr(args, 'func'):
        args.func(**vars(args))
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
