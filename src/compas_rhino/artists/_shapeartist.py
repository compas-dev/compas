from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas.utilities import is_color_rgb
from ._artist import Artist


__all__ = ['ShapeArtist']


class ShapeArtist(Artist):
    """Base class for artists for geometric shapes.

    Parameters
    ----------
    shape: :class:`compas.geometry.Shape`
        The geometry of the shape.
    color : tuple, optional
        The RGB color.
    layer : str, optional
        The layer in which the shape should be drawn.

    Attributes
    ----------
    shape: :class:`compas.geometry.Shape`
        The geometry of the shape.
    color : tuple
        The RGB color.
    layer : str
        The layer in which the shape should be drawn.
    default_color : tuple
        The default rgb color value of the shape (``(255, 255, 255)``).
    u : int
        The resolution in the u direction.
        The default is ``16`` and the minimum ``2``.
    v : int
        The resolution in the v direction.
        The default is ``16`` and the minimum ``2``.
    """

    default_color = (255, 255, 255)

    def __init__(self, shape, color=None, layer=None):
        super(ShapeArtist, self).__init__(shape, layer=layer)
        self._color = None
        self.color = color
        self._u = None
        self._v = None

    @property
    def shape(self):
        return self.item

    @shape.setter
    def shape(self, shape):
        self.item = shape

    @property
    def color(self):
        if not self._color:
            self._color = self.default_color
        return self._color

    @color.setter
    def color(self, color):
        if is_color_rgb(color):
            self._color = color

    @property
    def u(self):
        if not self._u:
            self._u = 16
        return self._u

    @u.setter
    def u(self, u):
        if u > 2:
            self._u = u

    @property
    def v(self):
        if not self._v:
            self._v = 16
        return self._v

    @v.setter
    def v(self, v):
        if v > 2:
            self._v = v
