from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino
from compas.datastructures import Mesh
from compas_rhino.artist import Artist

__all__ = ['ShapeArtist']


class ShapeArtist(Artist):
    """Base artist for drawing ``Shape`` objects.

    Examples
    --------
    >>>

    """

    __module__ = "compas_rhino.artists"

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
