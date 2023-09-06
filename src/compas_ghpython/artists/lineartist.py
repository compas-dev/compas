from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas.artists import GeometryArtist
from compas_rhino.conversions import line_to_rhino
from .artist import GHArtist


class LineArtist(GHArtist, GeometryArtist):
    """Artist for drawing lines.

    Parameters
    ----------
    line : :class:`~compas.geometry.Line`
        A COMPAS line.
    **kwargs : dict, optional
        Additional keyword arguments.
        See :class:`~compas_ghpython.artists.GHArtist` and :class:`~compas.artists.PrimitiveArtist` for more info.

    """

    def __init__(self, line, **kwargs):
        super(LineArtist, self).__init__(geometry=line, **kwargs)

    def draw(self):
        """Draw the line.

        Returns
        -------
        :rhino:`Rhino.Geometry.Line`

        """
        return line_to_rhino(self.geometry)
