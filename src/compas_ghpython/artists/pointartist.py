from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas_rhino import conversions

from compas.artists import GeometryArtist
from .artist import GHArtist


class PointArtist(GHArtist, GeometryArtist):
    """Artist for drawing points.

    Parameters
    ----------
    point : :class:`~compas.geometry.Point`
        A COMPAS point.
    **kwargs : dict, optional
        Additional keyword arguments.

    """

    def __init__(self, point, **kwargs):
        super(PointArtist, self).__init__(geometry=point, **kwargs)

    def draw(self):
        """Draw the point.

        Returns
        -------
        :rhino:`Rhino.Geometry.Point3d`

        """
        geometry = conversions.point_to_rhino(self.geometry)

        if self.transformation:
            geometry.Transform(conversions.transformation_to_rhino(self.transformation))

        return geometry
