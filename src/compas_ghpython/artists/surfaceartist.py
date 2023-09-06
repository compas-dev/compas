from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas.artists import GeometryArtist
from compas_rhino.conversions import surface_to_rhino
from .artist import GHArtist


class SurfaceArtist(GHArtist, GeometryArtist):
    """Artist for drawing surfaces.

    Parameters
    ----------
    surface : :class:`~compas.geometry.Surface`
        A COMPAS surface.

    Other Parameters
    ----------------
    **kwargs : dict, optional
        Additional keyword arguments.
        For more info, see :class:`GHArtist` and :class:`~compas.artists.SurfaceArtist`.

    """

    def __init__(self, surface, **kwargs):
        super(SurfaceArtist, self).__init__(geometry=surface, **kwargs)

    def draw(self):
        """Draw the surface.

        Returns
        -------
        :rhino:`Rhino.Geometry.Surface`

        """
        return surface_to_rhino(self.geometry)
