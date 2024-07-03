from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas.scene import GeometryObject
from compas_rhino import conversions

from .sceneobject import GHSceneObject


class PolyhedronObject(GHSceneObject, GeometryObject):
    """Scene object for drawing polyhedron shapes."""

    def draw(self):
        """Draw the polyhedron associated with the scene object.

        Parameters
        ----------
        color : tuple[int, int, int] | tuple[float, float, float] | :class:`compas.colors.Color`, optional
            The RGB color of the line.

        Returns
        -------
        list[:rhino:`Rhino.Geometry.Mesh`]
            List of created Rhino mesh.

        """
        color = self.surfacecolor
        vertices, faces = self.geometry.to_vertices_and_faces()

        geometry = conversions.vertices_and_faces_to_rhino(vertices, faces, color=color)
        geometry.Transform(conversions.transformation_to_rhino(self.worldtransformation))

        self._guids = [geometry]
        return self.guids
