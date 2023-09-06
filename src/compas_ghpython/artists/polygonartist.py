from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas.artists import GeometryArtist
from compas.colors import Color
from compas_rhino.conversions import vertices_and_faces_to_rhino
from compas_rhino.conversions import point_to_rhino
from compas_rhino.conversions import line_to_rhino
from .artist import GHArtist


class PolygonArtist(GHArtist, GeometryArtist):
    """Artist for drawing polygons.

    Parameters
    ----------
    polygon : :class:`~compas.geometry.Polygon`
        A COMPAS polygon.
    **kwargs : dict, optional
        Additional keyword arguments.
        See :class:`~compas_ghpython.artists.GHArtist` and :class:`~compas.artists.PrimitiveArtist` for more info.

    """

    def __init__(self, polygon, **kwargs):
        super(PolygonArtist, self).__init__(geometry=polygon, **kwargs)

    def draw(self, color=None, show_vertices=False, show_edges=False):
        """Draw the polygon.

        Parameters
        ----------
        color : tuple[int, int, int] | tuple[float, float, float] | :class:`~compas.colors.Color`, optional
            The RGB color of the polygon.
        show_vertices : bool, optional
            If True, draw the vertices of the polygon.
        show_edges : bool, optional
            If True, draw the edges of the polygon.

        Returns
        -------
        list[:rhino:`Rhino.Geometry.Point3d`, :rhino:`Rhino.Geometry.Line`, :rhino:`Rhino.Geometry.Mesh`]
            The Rhino points, lines and face.

        """
        color = Color.coerce(color) or self.color
        vertices = self.geometry.vertices
        faces = self.geometry.faces

        result = []
        result.append(vertices_and_faces_to_rhino(vertices, faces, color=color))

        if show_vertices:
            for point in vertices:
                result.append(point_to_rhino(point))

        if show_edges:
            for edge in self.geometry.edges:
                result.append(line_to_rhino([vertices[edge[0]], vertices[edge[1]]]))

        return result
