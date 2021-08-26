from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino
from compas_rhino.artists._shapeartist import ShapeArtist


class ConeArtist(ShapeArtist):

    def draw(self):
        """Draw the cone.

        Returns
        -------
        str
            The GUID of the created Rhino object.
        """
        vertices, faces = self.shape.to_vertices_and_faces(u=self.u)
        vertices = [list(vertex) for vertex in vertices]
        return compas_rhino.draw_mesh(vertices,
                                      faces,
                                      layer=self.layer,
                                      name=self.shape.name,
                                      color=self.color,
                                      disjoint=True,
                                      clear=False,
                                      redraw=False)
