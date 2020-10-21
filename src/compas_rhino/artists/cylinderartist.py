from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino
from ._shapeartist import ShapeArtist


class CylinderArtist(ShapeArtist):
    """Artist for drawing cylinder shapes.

    Parameters
    ----------
    shape : :class:`compas.geometry.Cylinder`
        A COMPAS cylinder.

    Notes
    -----
    See :class:`compas_rhino.artists.ShapeArtist` for all other parameters.

    """

    def draw(self, u=10, show_vertices=True):
        """Draw the cylinder associated with the artist.

        Parameters
        ----------
        u : int, optional
            Number of faces in the "u" direction.
            Default is ``10``.

        Returns
        -------
        list
            The GUIDs of the objects created in Rhino.
        """
        vertices, faces = self.shape.to_vertices_and_faces(u=u)
        vertices = [list(vertex) for vertex in vertices]
        guids = []
        if show_vertices:
            points = [{'pos': point, 'color': self.color} for point in vertices]
            guids += compas_rhino.draw_points(points, layer=self.layer, clear=False, redraw=False)
        polygons = [{'points': [vertices[index] for index in face], 'color': self.color} for face in faces]
        guids += compas_rhino.draw_faces(polygons, layer=self.layer, clear=False, redraw=False)
        self._guids = guids
        return guids


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':
    pass
