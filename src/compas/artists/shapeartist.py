from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas.colors import Color
from .artist import Artist


class ShapeArtist(Artist):
    """Base class for artists for geometric shapes.

    Parameters
    ----------
    shape: :class:`~compas.geometry.Shape`
        The geometry of the shape.
    color : tuple[float, float, float] | :class:`~compas.colors.Color`, optional
        The RGB color.

    Attributes
    ----------
    shape : :class:`~compas.geometry.Shape`
        The geometry of the shape.
    color : :class:`~compas.colors.Color`
        The color of the shape.
    u : int
        The resolution in the U direction of the discrete shape representation.
    v : int
        The resolution in the V direction of the discrete shape representation.

    Class Attributes
    ----------------
    default_color : :class:`~compas.colors.Color`
        The default color of the shape.

    """

    default_color = Color.from_hex("#0092D2")

    def __init__(self, shape, color=None, **kwargs):
        super(ShapeArtist, self).__init__()
        self._default_color = None

        self._u = None
        self._v = None
        self._shape = None
        self._color = None

        self.shape = shape
        self.color = color
        self.u = kwargs.get("u")
        self.v = kwargs.get("v")

    @property
    def shape(self):
        return self._shape

    @shape.setter
    def shape(self, shape):
        self._shape = shape

    @property
    def color(self):
        if not self._color:
            self.color = self.default_color
        return self._color

    @color.setter
    def color(self, value):
        self._color = Color.coerce(value)

    @property
    def u(self):
        if not self._u:
            self._u = 16
        return self._u

    @u.setter
    def u(self, u):
        if u and u > 3:
            self._u = u

    @property
    def v(self):
        if not self._v:
            self._v = 16
        return self._v

    @v.setter
    def v(self, v):
        if v and v > 3:
            self._v = v
