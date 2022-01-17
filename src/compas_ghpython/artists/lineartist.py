from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_ghpython
from compas.artists import PrimitiveArtist
from .artist import GHArtist


class LineArtist(GHArtist, PrimitiveArtist):
    """Artist for drawing lines.

    Parameters
    ----------
    line : :class:`compas.geometry.Line`
        A COMPAS line.
    **kwargs : dict, optional
        Additional keyword arguments.
        See :class:`compas_ghpython.artists.GHArtist` and :class:`compas.artists.PrimitiveArtist` for more info.

    """

    def __init__(self, line, **kwargs):
        super(LineArtist, self).__init__(primitive=line, **kwargs)

    def draw(self):
        """Draw the line.

        Returns
        -------
        :rhino:`Rhino.Geometry.Line`

        """
        lines = [self._get_args(self.primitive)]
        return compas_ghpython.draw_lines(lines)[0]

    @staticmethod
    def _get_args(primitive):
        start = list(primitive.start)
        end = list(primitive.end)
        return {'start': start, 'end': end}
