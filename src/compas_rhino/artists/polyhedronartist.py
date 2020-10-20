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

    """

    def draw(self):
        """Draw the polyhedron associated with the artist.

        Returns
        -------
        list
            The GUIDs of the objects created in Rhino.
        """
        vertices = [list(vertex) for vertex in self.shape.vertices]
        faces = self.shape.faces
        edges = self.shape.edges
        points = [{'pos': point, 'color': self.color} for point in vertices]
        lines = [{'start': vertices[i], 'end': vertices[j], 'color': self.color} for i, j in edges]
        polygons = [{'points': [vertices[index] for index in face], 'color': self.color} for face in faces]
        guids = compas_rhino.draw_points(points, layer=self.layer, clear=False, redraw=False)
        guids += compas_rhino.draw_lines(lines, layer=self.layer, clear=False, redraw=False)
        guids += compas_rhino.draw_faces(polygons, layer=self.layer, clear=False, redraw=False)
        self._guids = guids
        return guids


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':
    pass
