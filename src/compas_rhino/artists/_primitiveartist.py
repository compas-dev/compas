from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas.utilities import is_color_rgb
from ._artist import Artist


__all__ = ["PrimitiveArtist"]


class PrimitiveArtist(Artist):
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
    color : tuple
        The RGB components of the base color of the primitive.
    layer : str
        The layer in which the primitive should be contained.
    default_color : tuple
        The default rgb color value of the primitive (``(0, 0, 0)``).
    """

    default_color = (0, 0, 0)

    def __init__(self, primitive, color=None, layer=None):
        super(PrimitiveArtist, self).__init__(primitive, layer=layer)
        self._color = None
        self.color = color

    @property
    def primitive(self):
        return self.item

    @primitive.setter
    def primitive(self, primitive):
        self.item = primitive

    @property
    def color(self):
        if not self._color:
            self._color = self.default_color
        return self._color

    @color.setter
    def color(self, color):
        if is_color_rgb(color):
            self._color = color
