from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas.artists import SurfaceArtist
from .artist import GHArtist


class SurfaceArtist(GHArtist, SurfaceArtist):
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
        super(SurfaceArtist, self).__init__(surface=surface, **kwargs)

    def draw(self):
        """Draw the surface.

        Returns
        -------
        :rhino:`Rhino.Geometry.Surface`

        """
        return self.surface.rhino_surface
