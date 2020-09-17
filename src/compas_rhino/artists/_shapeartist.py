from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino
from compas.datastructures import Mesh
from compas_rhino.artists._artist import BaseArtist

__all__ = ['ShapeArtist']


class ShapeArtist(BaseArtist):
    """Base class for artists for geometric shapes.

    Parameters
    ----------
    shape: :class:`compas.geometry.Shape`
        The geometry of the shape.
    color : 3-tuple, optional
        The RGB components of the base color of the shape.
    layer : str, optional
        The layer in which the shape should be contained.

    Attributes
    ----------
    shape: :class:`compas.geometry.Shape`
        The geometry of the shape.
    name : str
        The name of the shape.
    color : tuple
        The RGB components of the base color of the shape.
    layer : str
        The layer in which the shape should be contained.

    """

    def __init__(self, shape, color=None, layer=None):
        super(ShapeArtist, self).__init__()
        self._shape = None
        self._mesh = None
        self.shape = shape
        self.color = color
        self.layer = layer

    @property
    def shape(self):
        """:class:`compas.geometry.Shape` : The geometry of the shape."""
        return self._shape

    @shape.setter
    def shape(self, shape):
        self._shape = shape
        self._mesh = Mesh.from_shape(shape)

    @property
    def name(self):
        """str : Reference to the name of the shape."""
        return self.shape.name

    @name.setter
    def name(self, name):
        self.shape.name = name

    def clear_layer(self):
        """Clear the main layer of the artist."""
        if self.layer:
            compas_rhino.clear_layer(self.layer)


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    pass
