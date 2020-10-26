from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino
from ._shapeartist import ShapeArtist


class PolyhedronArtist(ShapeArtist):
    """Artist for drawing polyhedron shapes.

    Parameters
    ----------
    shape : :class:`compas.geometry.Polyhedron`
        A COMPAS polyhedron.

    Notes
    -----
    See :class:`compas_rhino.artists.ShapeArtist` for all other parameters.

    Examples
    --------
    .. code-block:: python

        import random
        from compas.geometry import Pointcloud
        from compas.geometry import Polyhedron
        from compas.geometry import Translation
        from compas.utilities import i_to_rgb

        import compas_rhino
        from compas_rhino.artists import PolyhedronArtist

        pcl = Pointcloud.from_bounds(10, 10, 10, 100)
        tpl = Polyhedron.from_platonicsolid(12)

        compas_rhino.clear_layer("Test::PolyhedronArtist")

        for point in pcl.points:
            polyhedron = tpl.transformed(Translation.from_vector(point))
            artist = PolyhedronArtist(polyhedron, color=i_to_rgb(random.random()), layer="Test::PolyhedronArtist")
            artist.draw()
    """

    def draw(self, show_vertices=False, show_edges=False, show_faces=True, join_faces=True):
        """Draw the polyhedron associated with the artist.

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
            points = [{'pos': point, 'color': self.color, 'name': str(index)} for index, point in enumerate(vertices)]
            guids += compas_rhino.draw_points(points, layer=self.layer, clear=False, redraw=False)
        if show_edges:
            edges = self.shape.edges
            lines = [{'start': vertices[i], 'end': vertices[j], 'color': self.color} for i, j in edges]
            guids += compas_rhino.draw_lines(lines, layer=self.layer, clear=False, redraw=False)
        if show_faces:
            faces = self.shape.faces
            if join_faces:
                guid = compas_rhino.draw_mesh(vertices, faces, layer=self.layer, name=self.name, color=self.color, disjoint=True)
                guids.append(guid)
            else:
                polygons = [{'points': [vertices[index] for index in face], 'color': self.color} for face in faces]
                guids += compas_rhino.draw_faces(polygons, layer=self.layer, clear=False, redraw=False)
        self._guids = guids
        return guids


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':
    pass
