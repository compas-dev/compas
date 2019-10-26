from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino
from compas_rhino.artists import _Artist

__all__ = ['_ShapeArtist']


class _ShapeArtist(_Artist):
    """Base class for all ``Shape`` artists.

    Parameters
    ----------
    shape : :class:`compas.geometry.Shape`
        The instance of the shape.

    Attributes
    ----------
    shape : :class:`compas.geometry.Shape`
        A reference to the geometry of the shape.

    """

    __module__ = "compas_rhino.artists"

    def __init__(self, shape, **kwargs):
        super(_ShapeArtist, self).__init__(kwargs)
        self.shape = shape


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':
    pass
