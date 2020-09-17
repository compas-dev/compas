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
        lines = [self._get_args(self.primitive)]
        return compas_ghpython.draw_lines(lines)[0]

    @staticmethod
    def draw_collection(collection):
        """Draw the collection of lines.

        Parameters
        ----------
        collection : list of compas.geometry.Line
            A collection of ``Line`` objects.

        Returns
        -------
        list of :class:`Rhino.Geometry.Line`

        """
        lines = [LineArtist._get_args(primitive) for primitive in collection]
        return compas_ghpython.draw_lines(lines)

    @staticmethod
    def _get_args(primitive):
        start = list(primitive.start)
        end = list(primitive.end)
        return {'start': start, 'end': end}


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    pass
