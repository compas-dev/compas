from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino
from compas_rhino.artists._artist import BaseArtist


__all__ = ["PrimitiveArtist"]


class PrimitiveArtist(BaseArtist):
    """Base class for artists for geometry primitives.

    Parameters
    ----------
    primitive: :class:`compas.geometry.Primitive`
        The geometry of the primitive.
    color : 3-tuple, optional
        The RGB components of the base color of the primitive.
    layer : str, optional
        The layer in which the primitive should be contained.

    Attributes
    ----------
    primitive: :class:`compas.geometry.Primitive`
        The geometry of the primitive.
    name : str
        The name of the primitive.
    color : tuple
        The RGB components of the base color of the primitive.
    layer : str
        The layer in which the primitive should be contained.

    """

    def __init__(self, primitive, color=None, layer=None):
        super(PrimitiveArtist, self).__init__()
        self.primitive = primitive
        self.color = color
        self.layer = layer

    @property
    def name(self):
        """str : Reference to the name of the primitive."""
        return self.primitive.name

    @name.setter
    def name(self, name):
        self.primitive.name = name

    def clear_layer(self):
        """Clear the layer containing the artist."""
        if self.layer:
            compas_rhino.clear_layer(self.layer)


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':
    pass
