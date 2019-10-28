from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas_rhino.artists import _Artist

__all__ = ["_PrimitiveArtist"]


class _PrimitiveArtist(_Artist):
    """Base class for all ``Primitive`` artists.

    Parameters
    ----------
    primitive: :class:`compas.geometry.Primitive`
        The instance of the primitive.

    Attributes
    ----------
    primitive: :class:`compas.geometry.Primitive`
        A reference to the geometry of the primitive.

    """

    __module__ = "compas_rhino.artists"

    def __init__(self, primitive, **kwargs):
        super(_PrimitiveArtist, self).__init__(kwargs)
        self.primitive = primitive


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':
    pass
