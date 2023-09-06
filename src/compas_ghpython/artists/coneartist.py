from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas.artists import GeometryArtist
from compas.colors import Color
from compas_rhino.conversions import vertices_and_faces_to_rhino
from .artist import GHArtist


class ConeArtist(GHArtist, GeometryArtist):
    """Artist for drawing cone shapes.

    Parameters
    ----------
    shape : :class:`~compas.geometry.Cone`
        A COMPAS cone.
    **kwargs : dict, optional
        Additional keyword arguments.
        See :class:`~compas_ghpython.artists.GHArtist` and :class:`~compas.artists.ShapeArtist` for more info.

    """

    def __init__(self, cone, **kwargs):
        super(ConeArtist, self).__init__(geometry=cone, **kwargs)

    def draw(self, color=None, u=16):
        """Draw the cone associated with the artist.

        Parameters
        ----------
        color : tuple[int, int, int] | tuple[float, float, float] | :class:`~compas.colors.Color`, optional
            The RGB color of the cone.
        u : int, optional
            Number of faces in the "u" direction.

        Returns
        -------
        :rhino:`Rhino.Geometry.Mesh`

        """
        color = Color.coerce(color) or self.color
        vertices, faces = self.geometry.to_vertices_and_faces(u=u)
        return vertices_and_faces_to_rhino(vertices, faces, color=color)
