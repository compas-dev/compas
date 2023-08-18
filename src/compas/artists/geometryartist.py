from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas.colors import Color
from .artist import Artist
from .descriptors.color import ColorAttribute


class GeometryArtist(Artist):
    """Base class for artists for geometry objects.

    Parameters
    ----------
    geometry : :class:`~compas.geometry.Geometry`
        The geometry of the geometry.

    Attributes
    ----------
    geometry : :class:`~compas.geometry.Geometry`
        The geometry object associated with the artist.
    color : :class:`~compas.colors.Color`
        The color of the object.

    See Also
    --------
    :class:`compas.artists.CurveArtist`
    :class:`compas.artists.SurfaceArtist`
    :class:`compas.artists.ShapeArtist`

    """

    color = ColorAttribute(default=Color.black())

    def __init__(self, geometry, **kwargs):
        super(GeometryArtist, self).__init__()
        self.geometry = geometry
