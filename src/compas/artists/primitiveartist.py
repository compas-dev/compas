from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas.colors import Color
from .artist import Artist


class PrimitiveArtist(Artist):
    """Base class for artists for geometry primitives.

    Parameters
    ----------
    primitive: :class:`compas.geometry.Primitive`
        The geometry of the primitive.
    color : tuple[float, float, float] | :class:`~compas.colors.Color`, optional
        The RGB components of the base color of the primitive.

    Attributes
    ----------
    primitive : :class:`compas.geometry.Primitive`
        The geometric primitive associated with the artist.
    color : :class:`~compas.colors.Color`
        The color of the object.

    Class Attributes
    ----------------
    default_color : :class:`~compas.colors.Color`
        The default rgb color value of the primitive.

    """

    default_color = Color.from_hex('#0092D2')

    def __init__(self, primitive, color=None, **kwargs):
        super(PrimitiveArtist, self).__init__()
        self._primitive = None
        self._color = None
        self.primitive = primitive
        self.color = color

    @property
    def primitive(self):
        return self._primitive

    @primitive.setter
    def primitive(self, primitive):
        self._primitive = primitive

    @property
    def color(self):
        if not self._color:
            self.color = self.default_color
        return self._color

    @color.setter
    def color(self, c):
        if not c:
            return
        if Color.is_rgb255(c):
            self._color = Color.from_rgb255(c[0], c[1], c[2])
        elif Color.is_hex(c):
            self._color = Color.from_hex(c)
        else:
            self._color = Color(c[0], c[1], c[2])
