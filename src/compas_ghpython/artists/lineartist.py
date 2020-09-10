from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_ghpython
from compas_ghpython.artists._primitiveartist import PrimitiveArtist


__all__ = ['LineArtist']


class LineArtist(PrimitiveArtist):
    """Artist for drawing lines.

    Parameters
    ----------
    primitive : :class:`compas.geometry.Line`
        A COMPAS line.

    Other Parameters
    ----------------
    See :class:`compas_ghpython.artists.PrimitiveArtist` for all other parameters.

    """

    def draw(self):
        """Draw the line.

        Returns
        -------
        :class:`Rhino.Geometry.Line`

        """
        start = list(self.primitive.start)
        end = list(self.primitive.end)
        lines = [{'start': start, 'end': end}]
        return compas_ghpython.draw_lines(lines)[0]


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    pass
