from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas.artists import GeometryArtist
from compas_rhino.conversions import curve_to_rhino
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
        For more info, see :class:`GHArtist` and :class:`~compas.artists.CurveArtist`.

    """

    def __init__(self, curve, **kwargs):
        super(CurveArtist, self).__init__(geometry=curve, **kwargs)

    def draw(self):
        """Draw the curve.

        Returns
        -------
        :rhino:`Rhino.Geometry.Curve`

        """
        return curve_to_rhino(self.geometry)
