from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_ghpython
from compas.artists import ShapeArtist
from .artist import GHArtist


class CylinderArtist(GHArtist, ShapeArtist):
    """Artist for drawing cylinder shapes.

    Parameters
    ----------
    cylinder : :class:`compas.geometry.Cylinder`
        A COMPAS cylinder.
    """

    def __init__(self, cylinder, **kwargs):
        super(CylinderArtist, self).__init__(shape=cylinder, **kwargs)

    def draw(self, color=None, u=None):
        """Draw the cylinder associated with the artist.

        Parameters
        ----------
        color : tuple of float, optional
            The RGB color of the cylinder.
        u : int, optional
            Number of faces in the "u" direction.
            Default is ``~CylinderArtist.u``.

        Returns
        -------
        :class:`Rhino.Geometry.Mesh`
        """
        color = color or self.color
        u = u or self.u
        vertices, faces = self.shape.to_vertices_and_faces(u=u)
        vertices = [list(vertex) for vertex in vertices]
        mesh = compas_ghpython.draw_mesh(vertices,
                                         faces,
                                         color=color)
        return mesh
