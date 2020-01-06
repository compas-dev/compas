from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas_rhino.artists import Artist

__all__ = ["PrimitiveArtist"]


class PrimitiveArtist(Artist):
    """Base class for all artists for ``compas.geometry.Primitive``.

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
        super(PrimitiveArtist, self).__init__(**kwargs)
        self.primitive = primitive


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':
    pass
