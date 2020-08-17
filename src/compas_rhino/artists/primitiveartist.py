from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino
from compas_rhino.artists.base import BaseArtist

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
    layer : str, optional
        The parent layer of the object.

    Attributes
    ----------
    primitive: :class:`compas.geometry.Primitive`
        A reference to the geometry of the primitive.
    name : str
        The name of the primitive.
    color : tuple
        The RGB components of the base color of the primitive.
    layer : str
        The layer in which the primitive should be contained.

    """

    def __init__(self, primitive, name=None, color=None, layer=None):
        super(PrimitiveArtist, self).__init__()
        self.primitive = primitive
        self.name = name
        self.color = color
        self.layer = layer

    def clear_layer(self):
        """Clear the main layer of the artist."""
        if self.layer:
            compas_rhino.clear_layer(self.layer)
        else:
            compas_rhino.clear_current_layer()


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':
    pass
