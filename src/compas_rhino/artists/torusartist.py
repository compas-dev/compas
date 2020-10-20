from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino
from ._shapeartist import ShapeArtist


class TorusArtist(ShapeArtist):
    """Artist for drawing torus shapes.

    Parameters
    ----------
    shape : :class:`compas.geometry.Torus`
        A COMPAS torus.

    Notes
    -----
    See :class:`compas_rhino.artists.ShapeArtist` for all other parameters.

    """

    def draw(self, u=10, v=10):
        """Draw the torus associated with the artist.

        Parameters
        ----------
        u : int, optional
            Number of faces in the "u" direction.
            Default is ``10``.
        v : int, optional
            Number of faces in the "v" direction.
            Default is ``10``.

        Returns
        -------
        list
            The GUIDs of the objects created in Rhino.
        """
        vertices, faces = self.shape.to_vertices_and_faces(u=u, v=v)
        vertices = [list(vertex) for vertex in vertices]
        points = [{'pos': point, 'color': self.color} for point in vertices]
        polygons = [{'points': [vertices[index] for index in face], 'color': self.color} for face in faces]
        guids = compas_rhino.draw_points(points, layer=self.layer, clear=False, redraw=False)
        guids += compas_rhino.draw_faces(polygons, layer=self.layer, clear=False, redraw=False)
        self._guids = guids
        return guids


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':
    pass
