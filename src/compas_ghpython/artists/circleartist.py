from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas.artists import GeometryArtist
from compas_rhino.conversions import circle_to_rhino
from .artist import GHArtist


class CircleArtist(GHArtist, GeometryArtist):
    """Artist for drawing circles.

    Parameters
    ----------
    circle : :class:`~compas.geometry.Circle`
        A COMPAS circle.
    **kwargs : dict, optional
        Additional keyword arguments.
        See :class:`~compas_ghpython.artists.GHArtist` and :class:`~compas.artists.PrimitiveArtist` for more info.

    """

    def __init__(self, circle, **kwargs):
        super(CircleArtist, self).__init__(geometry=circle, **kwargs)

    def draw(self):
        """Draw the circle.

        Returns
        -------
        :rhino:`Rhino.Geometry.Circle`

        """
        return circle_to_rhino(self.geometry)
