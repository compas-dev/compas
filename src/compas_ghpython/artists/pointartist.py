from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas.artists import GeometryArtist
from compas_rhino.conversions import point_to_rhino
from .artist import GHArtist


class PointArtist(GHArtist, GeometryArtist):
    """Artist for drawing points.

    Parameters
    ----------
    point : :class:`~compas.geometry.Point`
        A COMPAS point.
    **kwargs : dict, optional
        Additional keyword arguments.
        See :class:`~compas_ghpython.artists.GHArtist` and :class:`~compas.artists.PrimitiveArtist` for more info.

    """

    def __init__(self, point, **kwargs):
        super(PointArtist, self).__init__(geometry=point, **kwargs)

    def draw(self):
        """Draw the point.

        Returns
        -------
        :rhino:`Rhino.Geometry.Point3d`

        """
        return point_to_rhino(self.geometry)
