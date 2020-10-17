from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas.utilities import pairwise
import compas_rhino
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

    def draw(self):
        """Draw the box associated with the artist.

        Returns
        -------
        list
            The GUIDs of the objects created in Rhino.
        """
        vertices = self.shape.vertices
        faces = self.shape.faces
        edges = list(pairwise(self.shape.bottom + self.shape.bottom[:1]))
        edges += list(pairwise(self.shape.top + self.shape.top[:1]))
        edges += list(zip(self.shape.bottom, self.shape.top))
        points = [{'pos': point, 'color': self.color} for point in vertices]
        lines = [{'start': vertices[i], 'end': vertices[j], 'color': self.color} for i, j in edges]
        polygons = [{'points': [vertices[index] for index in face], 'color': self.color} for face in faces]
        guids = compas_rhino.draw_points(points, layer=self.layer, clear=False, redraw=False)
        guids += compas_rhino.draw_lines(lines, layer=self.layer, clear=False, redraw=False)
        guids += compas_rhino.draw_faces(polygons, layer=self.layer, clear=False, redraw=False)
        self._guids = guids
        return guids
