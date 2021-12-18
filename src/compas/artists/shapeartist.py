from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas.utilities import is_color_rgb
from .artist import Artist


class ShapeArtist(Artist):
    """Base class for artists for geometric shapes.

    Parameters
    ----------
    shape: :class:`compas.geometry.Shape`
        The geometry of the shape.
    color : Tuple[:obj:`float`, :obj:`float`, :obj:`float`], optional
        The RGB color.
    """

    default_color = (1, 1, 1)
    """Tuple[:obj:`float`, :obj:`float`, :obj:`float`] -
    The default color of the shape.
    """

    def __init__(self, shape, color=None, **kwargs):
        super(ShapeArtist, self).__init__()
        self._u = None
        self._v = None
        self._shape = None
        self._color = None
        self.shape = shape
        self.color = color
        self.u = kwargs.get('u')
        self.v = kwargs.get('v')

    @property
    def shape(self):
        """:class:`compas.geometry.Shape` - The geometry of the shape."""
        return self._shape

    @shape.setter
    def shape(self, shape):
        self._shape = shape

    @property
    def color(self):
        """Tuple[:obj:`float`, :obj:`float`, :obj:`float`] - The color of the shape."""
        if not self._color:
            self._color = self.default_color
        return self._color

    @color.setter
    def color(self, color):
        if is_color_rgb(color):
            self._color = color

    @property
    def u(self):
        """:obj:`int` - The resolution in the U direction of the discrete shape representation."""
        if not self._u:
            self._u = 16
        return self._u

    @u.setter
    def u(self, u):
        if u and u > 3:
            self._u = u

    @property
    def v(self):
        """:obj:`int` - The resolution in the V direction of the discrete shape representation."""
        if not self._v:
            self._v = 16
        return self._v

    @v.setter
    def v(self, v):
        if v and v > 3:
            self._v = v
