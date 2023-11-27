from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from .artist import Artist
from .descriptors.color import ColorAttribute


class GeometryArtist(Artist):
    """Base class for artists for geometry objects.

    Parameters
    ----------
    geometry : :class:`compas.geometry.Geometry`
        The geometry of the geometry.

    Attributes
    ----------
    geometry : :class:`compas.geometry.Geometry`
        The geometry object associated with the artist.
    color : :class:`compas.colors.Color`
        The color of the object.

    """

    color = ColorAttribute(default=None)

    def __init__(self, geometry, **kwargs):
        super(GeometryArtist, self).__init__(item=geometry, **kwargs)
        self.geometry = geometry
