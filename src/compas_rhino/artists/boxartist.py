from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

try:
    basestring
except NameError:
    basestring = str

import compas_rhino
from compas.utilities import iterable_like
from ._shapeartist import ShapeArtist


class BoxArtist(ShapeArtist):
    """Artist for drawing box shapes.

    Parameters
    ----------
    shape : :class:`compas.geometry.Box`
        A COMPAS box.

    Notes
    -----
    See :class:`compas_rhino.artists.ShapeArtist` for all other parameters.

    """

    def draw(self, show_vertices=False, show_edges=False, show_faces=True, join_faces=True):
        """Draw the box associated with the artist.

        Parameters
        ----------
        show_vertices : bool, optional
            Default is ``False``.
        show_edges : bool, optional
            Default is ``False``.
        show_faces : bool, optional
            Default is ``True``.
        join_faces : bool, optional
            Default is ``True``.

        Returns
        -------
        list
            The GUIDs of the objects created in Rhino.
        """
        vertices = [list(vertex) for vertex in self.shape.vertices]
        guids = []
        if show_vertices:
            points = [{'pos': point, 'color': self.color, 'name': self.name} for point in vertices]
            guids += compas_rhino.draw_points(points, layer=self.layer, clear=False, redraw=False)
        if show_edges:
            edges = self.shape.edges
            lines = [{'start': vertices[i], 'end': vertices[j], 'color': self.color, 'name': self.name} for i, j in edges]
            guids += compas_rhino.draw_lines(lines, layer=self.layer, clear=False, redraw=False)
        if show_faces:
            faces = self.shape.faces
            if join_faces:
                guid = compas_rhino.draw_mesh(vertices, faces, layer=self.layer, name=self.name, color=self.color, disjoint=True)
                guids.append(guid)
            else:
                polygons = [{'points': [vertices[index] for index in face], 'color': self.color, 'name': self.name} for face in faces]
                guids += compas_rhino.draw_faces(polygons, layer=self.layer, clear=False, redraw=False)
        self._guids = guids
        return guids

    @staticmethod
    def draw_collection(collection,
                        names=None, colors=None,
                        show_vertices=False, show_edges=False, show_faces=True,
                        layer=None, clear=False,
                        add_to_group=False, group_name=None,
                        join_faces=True):
        """Draw a collection of boxes.

        Parameters
        ----------
        collection : list of :class:`compas.geometry.Box`
            A collection of boxes.
        names : list of str, optional
            Individual names.
        colors : color or list of color, optional
            A color specification as a single color or a list of individual colors.
        show_vertices : bool, optional
            Default is ``False``.
        show_edges : bool, optional
            Default is ``False``.
        show_faces : bool, optional
            Default is ``True``.
        layer : str, optional
            A layer path.
        clear : bool, optional
            Clear the layer before drawing.
        add_to_group : bool, optional
            Add the points to a group.
        group_name : str, optional
            Name of the group.
        join_faces : bool, optional
            Default is ``True``.

        Returns
        -------
        guids: list
            A list of GUIDs if the collection is not grouped.
        groupname: str
            The name of the group if the collection objects are grouped.

        Examples
        --------
        >>> import random
        >>> from compas.geometry import Pointcloud
        >>> from compas.geometry import Box
        >>> from compas.utilities import i_to_rgb
        >>> from compas_rhino.artists import BoxArtist

        >>> pcl = Pointcloud.from_bounds(10, 10, 10, 100)
        >>> tpl = Box.from_width_height_depth(0.3, 0.3, 0.3)

        >>> collection = []
        >>> colors = []
        >>> for point in pcl.points:
        ...     box = tpl.copy()
        ...     box.frame.point = point
        ...     collection.append(box)
        ...     colors.append(i_to_rgb(random.random()))

        >>> BoxArtist.draw_collection(collection, colors=colors, layer="Test::BoxArtist", clear=True)

        """
        if colors:
            if isinstance(colors[0], (int, float)):
                colors = iterable_like(collection, [colors], colors)
            else:
                colors = iterable_like(collection, colors, colors[0])
            colors = list(colors)
        if names:
            if isinstance(names, basestring):
                names = iterable_like(collection, [names], names)
            else:
                names = iterable_like(collection, names, names[0])
            names = list(names)

        guids = []

        for index, box in enumerate(collection):
            vertices = [list(vertex) for vertex in box.vertices]

            if show_vertices:
                points = [{'pos': vertex} for vertex in vertices]
                if colors:
                    for point in points:
                        point['color'] = colors[index]
                if names:
                    for point in points:
                        point['name'] = names[index]
                guids += compas_rhino.draw_points(points, layer=layer)

            if show_edges:
                lines = [{'start': vertices[i], 'end': vertices[j]} for i, j in box.edges]
                if colors:
                    for line in lines:
                        line['color'] = colors[index]
                if names:
                    for line in lines:
                        line['name'] = names[index]
                guids += compas_rhino.draw_lines(lines, layer=layer)

            if show_faces:
                if join_faces:
                    name = None if not names else names[index]
                    color = None if not colors else colors[index]
                    guid = compas_rhino.draw_mesh(vertices, box.faces, layer=layer, name=name, color=color, disjoint=True)
                    guids.append(guid)
                else:
                    polygons = [{'points': [vertices[i] for i in face]} for face in box.faces]
                    if colors:
                        for polygon in polygons:
                            polygon['color'] = colors[index]
                    if names:
                        for polygon in polygons:
                            polygon['name'] = names[index]
                    guids += compas_rhino.draw_faces(polygons, layer=layer)

        if not add_to_group:
            return guids

        group = compas_rhino.rs.AddGroup(group_name)
        if group:
            compas_rhino.rs.AddObjectsToGroup(guids, group)
        return group


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':
    pass
