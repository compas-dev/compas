from compas.remote import ThreadedServer
from compas.remote import RequestHandler

from compas.datastructures import Network
from compas.datastructures import network_is_planar


class NetworkRequestHandler(RequestHandler):

    def is_planar(self, data):
        network = Network.from_data(data)
        return network_is_planar(network)


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':

    server = ThreadedServer(request_handler=NetworkRequestHandler)
    server.start()
