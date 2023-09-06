from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas.artists import GeometryArtist
from compas.colors import Color
from compas_rhino.conversions import vertices_and_faces_to_rhino
from .artist import GHArtist


class TorusArtist(GHArtist, GeometryArtist):
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
        super(TorusArtist, self).__init__(geometry=torus, **kwargs)

    def draw(self, color=None, u=16, v=16):
        """Draw the torus associated with the artist.

        Parameters
        ----------
        color : tuple[int, int, int] | tuple[float, float, float] | :class:`~compas.colors.Color`, optional
            The RGB color of the torus.
        u : int, optional
            Number of faces in the "u" direction.
        v : int, optional
            Number of faces in the "v" direction.

        Returns
        -------
        :rhino:`Rhino.Geometry.Mesh`

        """
        color = Color.coerce(color) or self.color
        vertices, faces = self.geometry.to_vertices_and_faces(u=u, v=v)
        vertices = [list(vertex) for vertex in vertices]
        return vertices_and_faces_to_rhino(vertices, faces, color=color)
