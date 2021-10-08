from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino
from compas.artists import ShapeArtist
from .artist import RhinoArtist


class PolyhedronArtist(RhinoArtist, ShapeArtist):
    """Artist for drawing polyhedron shapes.

    Parameters
    ----------
    polyhedron : :class:`compas.geometry.Polyhedron`
        A COMPAS polyhedron.
    layer : str, optional
        The layer that should contain the drawing.
    """

    def __init__(self, polyhedron, layer=None, **kwargs):
        super(PolyhedronArtist, self).__init__(shape=polyhedron, layer=layer, **kwargs)

    def draw(self, color=None):
        """Draw the polyhedron associated with the artist.

        Parameters
        ----------
        color : tuple of float, optional
            The RGB color of the polyhedron.

        Returns
        -------
        list
            The GUIDs of the objects created in Rhino.
        """
        color = color or self.color
        vertices = [list(vertex) for vertex in self.shape.vertices]
        faces = self.shape.faces
        guid = compas_rhino.draw_mesh(vertices,
                                      faces,
                                      layer=self.layer,
                                      name=self.shape.name,
                                      color=color,
                                      disjoint=True)
        return [guid]
