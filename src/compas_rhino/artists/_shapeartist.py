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
    color : 3-tuple, optional
        The RGB components of the base color of the shape.
    layer : str, optional
        The layer in which the shape should be contained.

    Attributes
    ----------
    shape: :class:`compas.geometry.Shape`
        The geometry of the shape.
    name : str
        The name of the shape.
    color : tuple
        The RGB components of the base color of the shape.
    layer : str
        The layer in which the shape should be contained.

    """

    default_color = (255, 255, 255)

    def __init__(self, shape, color=None, layer=None):
        super(ShapeArtist, self).__init__(layer=layer)
        self._shape = None
        self._color = None
        self.shape = shape
        self.color = color

    @property
    def shape(self):
        """:class:`compas.geometry.Shape` : The geometry of the shape."""
        return self._shape

    @shape.setter
    def shape(self, shape):
        self._shape = shape

    @property
    def color(self):
        """tuple : The RGB color value."""
        if not self._color:
            self._color = self.default_color
        return self._color

    @color.setter
    def color(self, color):
        if is_color_rgb(color):
            self._color = color
