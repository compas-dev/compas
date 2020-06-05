from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino
from compas_rhino.artists import Artist

__all__ = ["PrimitiveArtist"]


class PrimitiveArtist(Artist):
    """Base class for all artists for ``compas.geometry.Primitive``.

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

    """

    def __init__(self, primitive, name=None, color=None, layer=None):
        super(PrimitiveArtist, self).__init__()
        self.primitive = primitive
        self.name = name
        self.color = color
        self.layer = layer

    @classmethod
    def from_data(cls, data):
        module, attr = data['dtype'].split('/')
        Primitive = getattr(__import__(module, fromlist=[attr]), attr)
        primitive = Primitive.from_data(data['value'])
        artist = cls(primitive)
        return artist

    def to_data(self):
        return self.primitive.to_data()

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
