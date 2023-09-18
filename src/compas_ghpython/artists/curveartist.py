from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas_rhino import conversions

from compas.artists import GeometryArtist
from .artist import GHArtist


class CurveArtist(GHArtist, GeometryArtist):
    """Artist for drawing curves.

    Parameters
    ----------
    curve : :class:`~compas.geometry.Curve`
        A COMPAS curve.

    Other Parameters
    ----------------
    **kwargs : dict, optional
        Additional keyword arguments.

    """

    def __init__(self, curve, **kwargs):
        super(CurveArtist, self).__init__(geometry=curve, **kwargs)

    def draw(self):
        """Draw the curve.

        Returns
        -------
        :rhino:`Rhino.Geometry.Curve`

        """
        geometry = conversions.curve_to_rhino(self.geometry)

        if self.transformation:
            transformation = conversions.transformation_to_rhino(self.transformation)
            geometry.Transform(transformation)

        return geometry
