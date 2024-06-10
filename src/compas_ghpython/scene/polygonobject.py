from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas.scene import GeometryObject
from compas_rhino import conversions

from .sceneobject import GHSceneObject


class PolygonObject(GHSceneObject, GeometryObject):
    """Scene object for drawing polygons."""

    def draw(self):
        """Draw the polygon.

        Returns
        -------
        list[:rhino:`Rhino.Geometry.Mesh`]

        """
        color = self.surfacecolor
        vertices = self.geometry.vertices
        faces = self.geometry.faces

        geometry = conversions.vertices_and_faces_to_rhino(vertices, faces, color=color)
        geometry.Transform(conversions.transformation_to_rhino(self.worldtransformation))

        self._guids = [geometry]
        return self.guids
