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


__all__ = ['CircleArtist']


class CircleArtist(PrimitiveArtist):
    """Artist for drawing circles.

    Parameters
    ----------
    primitive : :class:`compas.geometry.Circle`
        A COMPAS circle.

    Other Parameters
    ----------------
    See :class:`compas_rhino.artists.PrimitiveArtist` for all other parameters.

    """

    def draw(self):
        """Draw the circle.

        Returns
        -------
        list
            The GUIDs of the created Rhino objects.
        """
        point = list(self.primitive.plane.point)
        normal = list(self.primitive.plane.normal)
        radius = self.primitive.radius
        circles = [{'plane': [point, normal], 'radius': radius, 'color': self.color, 'name': self.name}]
        guids = compas_rhino.draw_circles(circles, layer=self.layer, clear=False, redraw=False)
        self.guids = guids
        return guids

    @staticmethod
    def draw_collection(collection, names=None, colors=None, layer=None, clear=False, add_to_group=False, group_name=None):
        """Draw a collection of circles.

        Parameters
        ----------
        collection : list of :class:`compas.geometry.Circle`
            A collection of circles.
        names : list of str, optional
            Individual names for the circles.
        colors : color or list of color, optional
            A color specification for the circles as a single color or a list of individual colors.
        layer : str, optional
            A layer path.
        clear : bool, optional
            Clear the layer before drawing.
        add_to_group : bool, optional
            Add the circles to a group.
        group_name : str, optional
            Name of the group.

        Returns
        -------
        list
            The GUIDs of the created Rhino objects.
        """
        circles = []
        for circle in collection:
            circles.append({'plane': [list(circle[0][0]), list(circle[0][1])], 'radius': circle[1]})
        if colors:
            if isinstance(colors[0], (int, float)):
                colors = iterable_like(collection, [colors], colors)
            else:
                colors = iterable_like(collection, colors, colors[0])
            for point, rgb in zip(circles, colors):
                circle['color'] = rgb
        if names:
            if isinstance(names, basestring):
                names = iterable_like(collection, [names], names)
            else:
                names = iterable_like(collection, names, names[0])
            for circle, name in zip(circles, names):
                circle['name'] = name
        guids = compas_rhino.draw_circles(circles, layer=layer, clear=clear)
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
