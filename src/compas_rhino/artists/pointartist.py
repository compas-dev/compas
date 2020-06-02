from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

try:
    basestring
except NameError:
    basestring = str

import compas_rhino
from compas.utilities import iterable_like
from compas_rhino.artists import PrimitiveArtist


__all__ = ['PointArtist']


class PointArtist(PrimitiveArtist):
    """Artist for drawing ``Point`` objects.

    Examples
    --------
    >>>

    """

    __module__ = "compas_rhino.artists"

    def draw(self):
        """Draw the point.

        Returns
        -------
        guid: str
            The GUID of the created Rhino object.

        """
        points = [{'pos': list(self.primitive), 'color': self.color, 'name': self.name}]
        self.guids = compas_rhino.draw_points(points, layer=self.layer, clear=False, redraw=False)

    @staticmethod
    def draw_collection(collection, color=None, name=None, layer=None, clear=False, group_collection=False, group_name=None):
        """Draw a collection of points.

        Parameters
        ----------
        collection : list of compas.geometry.Point
            A collection of ``Point`` objects.
        color : tuple or list of tuple (optional)
            Color specification of the points.
            If one RGB color is provided, it will be applied to all points.
            If a list of RGB colors is provided, these colors are applied to the corresponding points.
            A list of colors should have the same length as the collection, with one color per item.
            Default value is ``None`` in which case the default point color of the artist is used.
        name : str or list of str (optional)
            Name of each point.
            If only one name is provided, this name will be used for all points.
            If a list of names is provided, the list should contain a name for each point in the collection.
        layer : str (optional)
            The layer in which the objects of the collection should be created.
            Default is ``None``, in which case the default layer setting of the artist is used.
        clear : bool (optional)
            Clear the layer before drawing.
            Default is ``False``.
        group_collection : bool (optional)
            Flag for grouping the objects of the collection.
            Default is ``False``.
        group_name : str (optional).
            The name of the group.
            Default is ``None``.

        Returns
        -------
        guids: list
            A list of GUIDs if the collection is not grouped.
        groupname: str
            The name of the group if the collection objects are grouped.

        """
        compas_rhino.rs.EnableRedraw(False)
        points = [{'pos': list(point)} for point in collection]
        if color:
            if isinstance(color[0], (int, float)):
                colors = iterable_like(collection, [color], color)
            else:
                colors = iterable_like(collection, color, color[0])
            for point, rgb in zip(points, colors):
                point['color'] = rgb
        if name:
            if isinstance(name, basestring):
                names = iterable_like(collection, [name], name)
            else:
                names = iterable_like(collection, name, name[0])
            for point, name in zip(points, names):
                point['name'] = name
        guids = compas_rhino.draw_points(points, layer=layer, clear=clear, redraw=False)
        if not group_collection:
            return guids
        group = compas_rhino.rs.AddGroup(group_name)
        if group:
            compas_rhino.rs.AddObjectsToGroup(guids, group)
        compas_rhino.rs.EnableRedraw(True)
        return group


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    pass
