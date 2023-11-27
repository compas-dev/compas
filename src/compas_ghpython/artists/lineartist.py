from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas_rhino import conversions

from compas.artists import GeometryArtist
from .artist import GHArtist


class LineArtist(GHArtist, GeometryArtist):
    """Artist for drawing lines.

    Parameters
    ----------
    line : :class:`compas.geometry.Line`
        A COMPAS line.
    **kwargs : dict, optional
        Additional keyword arguments.

    """

    def __init__(self, line, **kwargs):
        super(LineArtist, self).__init__(geometry=line, **kwargs)

    def draw(self):
        """Draw the line.

        Returns
        -------
        :rhino:`Rhino.Geometry.Line`

        """
        geometry = conversions.line_to_rhino(self.geometry)

        if self.transformation:
            geometry.Transform(conversions.transformation_to_rhino(self.transformation))

        return geometry
