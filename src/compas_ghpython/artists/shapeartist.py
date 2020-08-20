from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas.datastructures import Mesh
from compas_rhino.artists.base import BaseArtist


__all__ = ['ShapeArtist']


class ShapeArtist(BaseArtist):
    """Base class for artists for geometric shapes.

    Parameters
    ----------
    shape: :class:`compas.geometry.Shape`
        The instance of the shape.
    name : str, optional
        The name of the shape.

    Attributes
    ----------
    shape: :class:`compas.geometry.Shape`
        A reference to the geometry of the shape.
    name : str
        The name of the shape.

    Examples
    --------
    >>>

    """

    def __init__(self, shape, name=None):
        super(ShapeArtist, self).__init__()
        self._shape = None
        self._mesh = None
        self.shape = shape
        self.name = name

    @property
    def shape(self):
        return self._shape

    @shape.setter
    def shape(self, shape):
        self._shape = shape
        self._mesh = Mesh.from_shape(shape)


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    pass
