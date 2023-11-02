"""
Minimal example of a "special" service.

Note that this service can be defined anywhere.
If the location is not on the PYTHONPATH, the location has to be provided.
For example, if the service is defined in the same directory as the client script:

proxy = Proxy(service="special", cwd=os.path.dirname(__file__))

"""
from compas.rpc import Server
from compas.rpc import Dispatcher


class SpecialService(Dispatcher):
    def __init__(self):
        super(SpecialService, self).__init__()

    def special(self):
        return "special"


def start_service(**kwargs):
    address = "0.0.0.0", 1753
    server = Server(address)
    service = SpecialService()
    server.register_instance(service)
    server.serve_forever()


# ==============================================================================
# main
# ==============================================================================

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()

    args, unknown = parser.parse_known_args()

    start_service()
