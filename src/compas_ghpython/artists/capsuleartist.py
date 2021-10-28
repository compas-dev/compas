from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_ghpython
from compas.artists import ShapeArtist
from .artist import GHArtist


class CapsuleArtist(GHArtist, ShapeArtist):
    """Artist for drawing capsule shapes.

    Parameters
    ----------
    capsule : :class:`compas.geometry.Capsule`
        A COMPAS capsule.
    """

    def __init__(self, capsule, **kwargs):
        super(CapsuleArtist, self).__init__(shape=capsule, **kwargs)

    def draw(self, color=None, u=None, v=None):
        """Draw the capsule associated with the artist.

        Parameters
        ----------
        color : tuple of float, optional
            The RGB color of the capsule.
        u : int, optional
            Number of faces in the "u" direction.
            Default is ``~CapsuleArtist.u``.
        v : int, optional
            Number of faces in the "v" direction.
            Default is ``~CapsuleArtist.v``.

        Returns
        -------
        :class:`Rhino.Geometry.Mesh`
        """
        color = color or self.color
        u = u or self.u
        v = v or self.v
        vertices, faces = self.shape.to_vertices_and_faces(u=u, v=v)
        vertices = [list(vertex) for vertex in vertices]
        mesh = compas_ghpython.draw_mesh(vertices,
                                         faces,
                                         color=color)
        return mesh
