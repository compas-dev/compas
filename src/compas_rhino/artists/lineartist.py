from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

# from itertools import zip_longest

import compas_rhino
# from compas.utilities import like_list
from compas_rhino.artists import _PrimitiveArtist


__all__ = ['LineArtist']


def list_like(target, value, fillvalue=None):
    p = len(target)

    if isinstance(value, list):
        matched_list = value
    else:
        matched_list = [value] * p

    d = len(matched_list)
    if d < p:
        matched_list.extend([fillvalue] * (p - d))

    return matched_list


class LineArtist(_PrimitiveArtist):
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

    __module__ = "compas_rhino.artists"

    def __init__(self, line, layer=None):
        super(LineArtist, self).__init__(line, layer=layer)
        self.settings.update({
            'color.line': (0, 0, 0)})

    def draw(self):
        """Draw the line.

        Returns
        -------
        guid: str
            The GUID of the created Rhino object.

        """
        start = list(self.primitive.start)
        end = list(self.primitive.end)
        lines = [{'start': start, 'end': end, 'color': self.settings['color.Line']}]
        guids = compas_rhino.draw_lines(lines, layer=self.settings['layer'], clear=False)
        if guids:
            return guids[0]

    @staticmethod
    def draw_collection(collection, color=None, layer=None, clear=False, group_collection=False, group_name=None):
        """Draw a collection of lines.

        Parameters
        ----------
        collection: list of compas.geometry.Line
            A collection of ``Line`` objects.
        color: tuple or list of tuple (optional)
            Color specification of the lines.
            If one RGB color is provided, it will be applied to all lines.
            If a list of RGB colors is provided, these colors are applied to the corresponding lines.
            A list of colors should have the same length as the collection, with one color per item.
            Default value is ``None`` in which case the default line color of the artist is used.
        layer: str (optional)
            The layer in which the objects of the collection should be created.
            Default is ``None``, in which case the default layer setting of the artist is used.
        clear: bool (optional)
            Clear the layer before drawing.
            Default is ``False``.
        group_collection: bool (optional)
            Flag for grouping the objects of the collection.
            Default is ``False``.
        group_name: str (optional).
            The name of the group.
            Default is ``None``.

        Returns
        -------
        guids: list
            A list of GUIDs if the collection is not grouped.
        groupname: str
            The name of the group if the collection objects are grouped.

        """
        colors = list_like(collection, color)
        lines = []
        for line, rgb in zip(collection, colors):
            lines.append({
                'start': list(line.start),
                'end': list(line.end),
                'color': rgb})
        guids = compas_rhino.draw_lines(lines, layer=layer, clear=clear)
        if not group_collection:
            return guids
        group = compas_rhino.rs.AddGroup(group_name)
        if group:
            compas_rhino.rs.AddObjectsToGroup(guids, group)
        return group


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    pass
