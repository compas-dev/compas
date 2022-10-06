from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_ghpython
from compas.artists import ShapeArtist
from compas.colors import Color
from .artist import GHArtist


class TorusArtist(GHArtist, ShapeArtist):
    """Artist for drawing torus shapes.

    Parameters
    ----------
    torus : :class:`~compas.geometry.Torus`
        A COMPAS torus.
    **kwargs : dict, optional
        Additional keyword arguments.
        See :class:`~compas_ghpython.artists.GHArtist` and :class:`~compas.artists.ShapeArtist` for more info.

    """

    def __init__(self, torus, **kwargs):
        super(TorusArtist, self).__init__(shape=torus, **kwargs)

    def draw(self, color=None, u=None, v=None):
        """Draw the torus associated with the artist.

        Parameters
        ----------
        color : tuple[int, int, int] | tuple[float, float, float] | :class:`~compas.colors.Color`, optional
            The RGB color of the torus.
            Default is :attr:`compas.artists.ShapeArtist.color`.
        u : int, optional
            Number of faces in the "u" direction.
            Default is :attr:`TorusArtist.u`
        v : int, optional
            Number of faces in the "v" direction.
            Default is :attr:`TorusArtist.v`.

        Returns
        -------
        :rhino:`Rhino.Geometry.Mesh`

        """
        color = Color.coerce(color) or self.color
        u = u or self.u
        v = v or self.v
        vertices, faces = self.shape.to_vertices_and_faces(u=u, v=v)
        vertices = [list(vertex) for vertex in vertices]
        mesh = compas_ghpython.draw_mesh(vertices, faces, color=color.rgb255)
        return mesh
