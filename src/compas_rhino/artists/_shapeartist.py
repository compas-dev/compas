from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

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
        super(ShapeArtist, self).__init__(shape, color=color, layer=layer)
        self._u = None
        self._v = None

    @property
    def shape(self):
        return self.item

    @shape.setter
    def shape(self, shape):
        self.item = shape

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
