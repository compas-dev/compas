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


__all__ = ['PointArtist']


class PointArtist(PrimitiveArtist):
    """Artist for drawing points.

    Parameters
    ----------
    primitive : :class:`compas.geometry.Point`
        A COMPAS point.

    Other Parameters
    ----------------
    See :class:`compas_rhino.artists.PrimitiveArtist` for all other parameters.

    Examples
    --------
    >>>

    """

    def draw(self):
        """Draw the point.

        Returns
        -------
        list
            The GUIDs of the created Rhino objects.

        """
        points = [{'pos': list(self.primitive), 'color': self.color, 'name': self.name}]
        guids = compas_rhino.draw_points(points, layer=self.layer, clear=False, redraw=False)
        self.guids = guids
        return guids

    @staticmethod
    def draw_collection(collection, names=None, colors=None, layer=None, clear=False, add_to_group=False, group_name=None):
        """Draw a collection of points.

        Parameters
        ----------
        collection : list of :class:`compas.geometry.Point`
            A collection of points.
        names : list of str, optional
            Individual names for the points.
        colors : color or list of color, optional
            A color specification for the points as a single color or a list of individual colors.
        layer : str, optional
            A layer path.
        clear : bool, optional
            Clear the layer before drawing.
        add_to_group : bool, optional
            Add the points to a group.
        group_name : str, optional
            Name of the group.

        Returns
        -------
        guids: list
            A list of GUIDs if the collection is not grouped.
        groupname: str
            The name of the group if the collection objects are grouped.

        """
        points = [{'pos': list(point)} for point in collection]
        if colors:
            if isinstance(colors[0], (int, float)):
                colors = iterable_like(collection, [colors], colors)
            else:
                colors = iterable_like(collection, colors, colors[0])
            for point, rgb in zip(points, colors):
                point['color'] = rgb
        if names:
            if isinstance(names, basestring):
                names = iterable_like(collection, [names], names)
            else:
                names = iterable_like(collection, names, names[0])
            for point, name in zip(points, names):
                point['name'] = name
        guids = compas_rhino.draw_points(points, layer=layer, clear=clear)
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
