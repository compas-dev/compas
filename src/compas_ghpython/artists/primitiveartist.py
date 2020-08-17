from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas_ghpython.artists.base import BaseArtist


__all__ = ["PrimitiveArtist"]


class PrimitiveArtist(BaseArtist):
    """Base class for artists for geometry primitives.

    Parameters
    ----------
    primitive: :class:`compas.geometry.Primitive`
        The instance of the primitive.
    name : str, optional
        The name of the primitive object.
    color : 3-tuple, optional
        The RGB color specification of the object.

    Attributes
    ----------
    primitive: :class:`compas.geometry.Primitive`
        A reference to the geometry of the primitive.
    name : str
        The name of the primitive.
    color : tuple
        The RGB components of the base color of the primitive.

    """

    def __init__(self, primitive, name=None, color=None):
        super(PrimitiveArtist, self).__init__()
        self.primitive = primitive
        self.name = name
        self.color = color


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':
    pass
