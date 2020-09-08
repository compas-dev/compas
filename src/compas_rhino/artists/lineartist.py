from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

try:
    basestring
except NameError:
    basestring = str

import compas_rhino
from compas.utilities import iterable_like
from compas_rhino.artists._primitiveartist import PrimitiveArtist


__all__ = ['LineArtist']


class LineArtist(PrimitiveArtist):
    """Artist for drawing lines.

    Parameters
    ----------
    primitive : :class:`compas.geometry.Line`
        A COMPAS line.

    Notes
    -----
    See :class:`compas_rhino.artists.PrimitiveArtist` for all other parameters.

    """

    def draw(self):
        """Draw the line.

        Returns
        -------
        list
            The GUIDs of the created Rhino objects.

        """
        start = list(self.primitive.start)
        end = list(self.primitive.end)
        lines = [{'start': start, 'end': end, 'color': self.color, 'name': self.name}]
        guids = compas_rhino.draw_lines(lines, layer=self.layer, clear=False, redraw=False)
        self.guids = guids
        return guids

    @staticmethod
    def draw_collection(collection, names=None, colors=None, layer=None, clear=False, add_to_group=False, group_name=None):
        """Draw a collection of lines.

        Parameters
        ----------
        collection: list of compas.geometry.Line
            A collection of ``Line`` objects.
        names : list of str, optional
            Individual names for the lines.
        colors : color or list of color, optional
            A color specification for the lines as a single color or a list of individual colors.
        layer : str, optional
            A layer path.
        clear : bool, optional
            Clear the layer before drawing.
        add_to_group : bool, optional
            Add the frames to a group.
        group_name : str, optional
            Name of the group.

        Returns
        -------
        guids: list
            A list of GUIDs if the collection is not grouped.
        groupname: str
            The name of the group if the collection objects are grouped.

        """
        lines = [{'start': list(line[0]), 'end': list(line[1])} for line in collection]
        if colors:
            if isinstance(colors[0], (int, float)):
                colors = iterable_like(collection, [colors], colors)
            else:
                colors = iterable_like(collection, colors, colors[0])
            for line, rgb in zip(lines, colors):
                line['color'] = rgb
        if names:
            if isinstance(names, basestring):
                names = iterable_like(collection, [names], names)
            else:
                names = iterable_like(collection, names, names[0])
            for line, name in zip(lines, names):
                line['name'] = name
        guids = compas_rhino.draw_lines(lines, layer=layer, clear=clear)
        if not add_to_group:
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
