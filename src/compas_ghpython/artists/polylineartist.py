from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas.artists import GeometryArtist
from compas_rhino.conversions import polyline_to_rhino_curve
from .artist import GHArtist


class PolylineArtist(GHArtist, GeometryArtist):
    """Artist for drawing polylines.

    Parameters
    ----------
    polyline : :class:`~compas.geometry.Polyline`
        A COMPAS polyline.
    **kwargs : dict, optional
        Additional keyword arguments.
        See :class:`~compas_ghpython.artists.GHArtist` and :class:`~compas.artists.PrimitiveArtist` for more info.

    """

    def __init__(self, polyline, **kwargs):
        super(PolylineArtist, self).__init__(geometry=polyline, **kwargs)

    def draw(self):
        """Draw the polyline.

        Returns
        -------
        :rhino:`Rhino.Geometry.PolylineCurve`.

        """
        return polyline_to_rhino_curve(self.geometry)
