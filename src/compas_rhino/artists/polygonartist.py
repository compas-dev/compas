from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import scriptcontext as sc  # type: ignore

from compas.artists import GeometryArtist
from compas.colors import Color
from compas_rhino.conversions import point_to_rhino
from compas_rhino.conversions import line_to_rhino
from compas_rhino.conversions import vertices_and_faces_to_rhino
from .artist import RhinoArtist
from ._helpers import attributes


class PolygonArtist(RhinoArtist, GeometryArtist):
    """Artist for drawing polygons.

    Parameters
    ----------
    polygon : :class:`~compas.geometry.Polygon`
        A COMPAS polygon.
    **kwargs : dict, optional
        Additional keyword arguments.
        For more info, see :class:`RhinoArtist` and :class:`GeometryArtist`.

    """

    def __init__(self, polygon, **kwargs):
        super(PolygonArtist, self).__init__(geometry=polygon, **kwargs)

    def draw(self, color=None, show_points=False, show_edges=False):
        """Draw the polygon.

        Parameters
        ----------
        color : tuple[int, int, int] | tuple[float, float, float] | :class:`~compas.colors.Color`, optional
            The RGB color of the polygon.
            Default is :attr:`compas.artists.GeometryArtist.color`.
        show_points : bool, optional
            If True, draw the corner points of the polygon.
        show_edges : bool, optional
            If True, draw the boundary edges of the polygon.

        Returns
        -------
        list[System.Guid]
            The GUIDs of the created Rhino objects.

        """
        color = Color.coerce(color) or self.color
        attr = attributes(name=self.geometry.name, color=color, layer=self.layer)

        guids = []

        vertices = self.geometry.points
        faces = self.geometry.faces
        mesh = vertices_and_faces_to_rhino(vertices, faces)
        guid = sc.doc.Objects.AddMesh(mesh, attr)
        guids.append(guid)

        if show_points:
            for point in self.geometry.points:
                guid = sc.doc.Objects.AddPoint(point_to_rhino(point), attr)
                guids.append(guid)

        if show_edges:
            for line in self.geometry.lines:
                guid = sc.doc.Objects.AddLine(line_to_rhino(line), attr)
                guids.append(guid)
