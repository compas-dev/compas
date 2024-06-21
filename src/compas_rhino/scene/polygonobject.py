from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import scriptcontext as sc  # type: ignore

from compas.scene import GeometryObject
from compas_rhino.conversions import transformation_to_rhino
from compas_rhino.conversions import vertices_and_faces_to_rhino

from .sceneobject import RhinoSceneObject


class RhinoPolygonObject(RhinoSceneObject, GeometryObject):
    """Scene object for drawing polygons."""

    def draw(self):
        """Draw the polygon.

        Returns
        -------
        list[System.Guid]
            List of GUIDs of the objects created in Rhino.

        """
        attr = self.compile_attributes()
        vertices = self.geometry.points
        faces = self.geometry.faces
        mesh = vertices_and_faces_to_rhino(vertices, faces)
        mesh.Transform(transformation_to_rhino(self.worldtransformation))

        self._guids = [sc.doc.Objects.AddMesh(mesh, attr)]
        return self.guids
