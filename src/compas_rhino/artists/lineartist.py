from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino
# from compas.utilities import iterable_like
from compas_rhino.artists import PrimitiveArtist


__all__ = ['LineArtist']


class LineArtist(PrimitiveArtist):
    """Artist for drawing ``Line`` objects.

    Parameters
    ----------
    line : :class:`compas.geometry.Line`
        A COMPAS line.
    layer : str (optional)
        The name of the layer that will contain the line.
        Default value is ``None``, in which case the current layer will be used.

    Examples
    --------
    >>>

    """

    def draw(self):
        """Draw the line.

        """
        start = list(self.primitive.start)
        end = list(self.primitive.end)
        lines = [{'start': start, 'end': end, 'color': self.color, 'name': self.name}]
        self.guids = compas_rhino.draw_lines(lines, layer=self.layer, clear=False, redraw=False)

    # @staticmethod
    # def draw_collection(collection, color=None, layer=None, clear=False, group_collection=False, group_name=None):
    #     """Draw a collection of lines.

    #     Parameters
    #     ----------
    #     collection: list of compas.geometry.Line
    #         A collection of ``Line`` objects.
    #     color: tuple or list of tuple (optional)
    #         Color specification of the lines.
    #         If one RGB color is provided, it will be applied to all lines.
    #         If a list of RGB colors is provided, these colors are applied to the corresponding lines.
    #         A list of colors should have the same length as the collection, with one color per item.
    #         Default value is ``None`` in which case the default line color of the artist is used.
    #     layer: str (optional)
    #         The layer in which the objects of the collection should be created.
    #         Default is ``None``, in which case the default layer setting of the artist is used.
    #     clear: bool (optional)
    #         Clear the layer before drawing.
    #         Default is ``False``.
    #     group_collection: bool (optional)
    #         Flag for grouping the objects of the collection.
    #         Default is ``False``.
    #     group_name: str (optional).
    #         The name of the group.
    #         Default is ``None``.

    #     Returns
    #     -------
    #     guids: list
    #         A list of GUIDs if the collection is not grouped.
    #     groupname: str
    #         The name of the group if the collection objects are grouped.

    #     """
    #     colors = iterable_like(collection, color)
    #     lines = []
    #     for line, rgb in zip(collection, colors):
    #         lines.append({
    #             'start': list(line.start),
    #             'end': list(line.end),
    #             'color': rgb})
    #     guids = compas_rhino.draw_lines(lines, layer=layer, clear=clear)
    #     if not group_collection:
    #         return guids
    #     group = compas_rhino.rs.AddGroup(group_name)
    #     if group:
    #         compas_rhino.rs.AddObjectsToGroup(guids, group)
    #     return group


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    pass
