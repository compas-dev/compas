from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import scriptcontext as sc  # type: ignore

from compas.scene import GeometryObject
from compas.colors import Color
from compas_rhino.conversions import point_to_rhino
from compas_rhino.conversions import line_to_rhino
from compas_rhino.conversions import vertices_and_faces_to_rhino
from compas_rhino.conversions import transformation_to_rhino
from .sceneobject import RhinoSceneObject
from ._helpers import attributes


class PolygonObject(RhinoSceneObject, GeometryObject):
    """Scene object for drawing polygons.

    Parameters
    ----------
    polygon : :class:`compas.geometry.Polygon`
        A COMPAS polygon.
    **kwargs : dict, optional
        Additional keyword arguments.

    """

    def __init__(self, polygon, **kwargs):
        super(PolygonObject, self).__init__(geometry=polygon, **kwargs)

    def draw(self, color=None):
        """Draw the polygon.

        Parameters
        ----------
        color : rgb1 | rgb255 | :class:`compas.colors.Color`, optional
            The RGB color of the polygon.

        Returns
        -------
        System.Guid
            The GUID of the created Rhino object.

        """
        color = Color.coerce(color) or self.color
        attr = attributes(name=self.geometry.name, color=color, layer=self.layer)

        vertices = self.geometry.points
        faces = self.geometry.faces
        mesh = vertices_and_faces_to_rhino(vertices, faces)
        if self.transformation:
            mesh.Transform(transformation_to_rhino(self.transformation))

        return sc.doc.Objects.AddMesh(mesh, attr)

    def draw_vertices(self, color=None):
        """Draw the polygon vertices.

        Parameters
        ----------
        color : rgb1 | rgb255 | :class:`compas.colors.Color`, optional
            The RGB color of the polygon vertices.

        Returns
        -------
        list[System.Guid]
            The GUIDs of the created Rhino objects.

        """
        color = Color.coerce(color) or self.color
        attr = attributes(name=self.geometry.name, color=color, layer=self.layer)

        guids = []

        for point in self.geometry.points:
            guid = sc.doc.Objects.AddPoint(point_to_rhino(point), attr)
            guids.append(guid)

        return guids

    def draw_edges(self, color=None):
        """Draw the polygon edges.

        Parameters
        ----------
        color : rgb1 | rgb255 | :class:`compas.colors.Color`, optional
            The RGB color of the polygon edges.

        Returns
        -------
        list[System.Guid]
            The GUIDs of the created Rhino objects.

        """
        color = Color.coerce(color) or self.color
        attr = attributes(name=self.geometry.name, color=color, layer=self.layer)

        guids = []

        for line in self.geometry.lines:
            guid = sc.doc.Objects.AddLine(line_to_rhino(line), attr)
            guids.append(guid)

        return guids
