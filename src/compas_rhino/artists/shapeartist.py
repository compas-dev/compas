from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino
from compas.datastructures import Mesh
from compas_rhino.artists import Artist

__all__ = ['ShapeArtist']


class ShapeArtist(Artist):
    """Base class for artists for geometric shapes.

    Examples
    --------
    >>>

    """

    def __init__(self, shape, name=None, layer=None):
        super(ShapeArtist, self).__init__()
        self._shape = None
        self._mesh = None
        self.shape = shape
        self.name = name
        self.layer = layer

    @property
    def shape(self):
        return self._shape

    @shape.setter
    def shape(self, shape):
        self._shape = shape
        self._mesh = Mesh.from_shape(shape)

    # @classmethod
    # def from_data(cls, data):
    #     module, attr = data['dtype'].split('/')
    #     Shape = getattr(__import__(module, fromlist=[attr]), attr)
    #     shape = Shape.from_data(data['value'])
    #     artist = cls(shape)
    #     return artist

    # def to_data(self):
    #     return self.shape.to_data()

    def draw(self):
        raise NotImplementedError

    def clear_layer(self):
        """Clear the main layer of the artist."""
        if self.layer:
            compas_rhino.clear_layer(self.layer)
        else:
            compas_rhino.clear_current_layer()


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    pass
