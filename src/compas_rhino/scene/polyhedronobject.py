from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import scriptcontext as sc  # type: ignore

from compas.scene import GeometryObject
from compas_rhino.conversions import transformation_to_rhino
from compas_rhino.conversions import vertices_and_faces_to_rhino

from .sceneobject import RhinoSceneObject


class RhinoPolyhedronObject(RhinoSceneObject, GeometryObject):
    """Scene object for drawing polyhedron shapes."""

    def draw(self):
        """Draw the polyhedron associated with the scene object.

        Returns
        -------
        list[System.Guid]
            The GUIDs of the objects created in Rhino.

        """
        attr = self.compile_attributes()
        vertices = [list(vertex) for vertex in self.geometry.vertices]
        faces = self.geometry.faces
        geometry = vertices_and_faces_to_rhino(vertices, faces)
        geometry.Transform(transformation_to_rhino(self.worldtransformation))

        self._guids = [sc.doc.Objects.AddMesh(geometry, attr)]
        return self.guids
