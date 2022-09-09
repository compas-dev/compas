from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_ghpython
from compas.artists import PrimitiveArtist
from compas.colors import Color
from .artist import GHArtist


class LineArtist(GHArtist, PrimitiveArtist):
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
        super(LineArtist, self).__init__(primitive=line, **kwargs)

    def draw(self, color=None):
        """Draw the line.

        Parameters
        ----------
        color : tuple[int, int, int] | tuple[float, float, float] | :class:`~compas.colors.Color`, optional
            The RGB color of the line.
            Default is :attr:`compas.artists.PrimitiveArtist.color`.

        Returns
        -------
        :rhino:`Rhino.Geometry.Line`

        """
        color = Color.coerce(color) or self.color
        start = list(self.primitive.start)
        end = list(self.primitive.end)
        lines = [{"start": start, "end": end, "color": color.rgb255}]
        return compas_ghpython.draw_lines(lines)[0]
