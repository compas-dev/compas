from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_ghpython
from compas.artists import ShapeArtist
from .artist import GHArtist


class PolyhedronArtist(GHArtist, ShapeArtist):
    """Artist for drawing polyhedron shapes.

    Parameters
    ----------
    polyhedron : :class:`compas.geometry.Polyhedron`
        A COMPAS polyhedron.
    """

    def __init__(self, polyhedron, **kwargs):
        super(PolyhedronArtist, self).__init__(shape=polyhedron, **kwargs)

    def draw(self, color=None):
        """Draw the polyhedron associated with the artist.

        Parameters
        ----------
        color : tuple of float, optional
            The RGB color of the polyhedron.

        Returns
        -------
        :class:`Rhino.Geometry.Mesh`
        """
        color = color or self.color
        vertices = [list(vertex) for vertex in self.shape.vertices]
        faces = self.shape.faces
        mesh = compas_ghpython.draw_mesh(vertices,
                                         faces,
                                         color=color)
        return mesh
