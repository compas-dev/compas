from compas_blender.artists import Artist
from compas_blender.artists.mixins import VertexArtist
from compas_blender.artists.mixins import EdgeArtist


__all__ = [
    'NetworkArtist',
]


class NetworkArtist(EdgeArtist, VertexArtist, Artist):

    __module__ = "compas_blender.artists"

    def __init__(self, network, layer=None):
        super().__init__(layer=layer)
        self.network = network
        self.defaults.update({
            'color.vertex': [255, 255, 255],
            'color.edge':   [0, 0, 0],
        })

    @property
    def network(self):
        return self.datastructure

    @network.setter
    def network(self, network):
        self.datastructure = network

    def draw(self):
        raise NotImplementedError

    def clear(self):
        self.clear_vertices()
        self.clear_edges()


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    pass
