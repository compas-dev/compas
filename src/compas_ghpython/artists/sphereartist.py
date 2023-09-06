from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas.artists import GeometryArtist
from compas.colors import Color
from compas_rhino.conversions import vertices_and_faces_to_rhino
from .artist import GHArtist


class SphereArtist(GHArtist, GeometryArtist):
    """Artist for drawing sphere shapes.

    Parameters
    ----------
    sphere : :class:`~compas.geometry.Sphere`
        A COMPAS sphere.
    **kwargs : dict, optional
        Additional keyword arguments.
        See :class:`~compas_ghpython.artists.GHArtist` and :class:`~compas.artists.ShapeArtist` for more info.

    """

    def __init__(self, sphere, **kwargs):
        super(SphereArtist, self).__init__(geometry=sphere, **kwargs)

    def draw(self, color=None, u=16, v=16):
        """Draw the sphere associated with the artist.

        Parameters
        ----------
        color : tuple[int, int, int] | tuple[flot, float, float] | :class:`~compas.colors.Color`, optional
            The RGB color of the sphere.
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
        return vertices_and_faces_to_rhino(vertices, faces, color=color)
