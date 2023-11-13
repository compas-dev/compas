from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import scriptcontext as sc  # type: ignore

from compas.scene import GeometryObject
from compas.colors import Color
from compas_rhino.conversions import vertices_and_faces_to_rhino
from compas_rhino.conversions import transformation_to_rhino
from .sceneobject import RhinoSceneObject
from ._helpers import attributes


class PolyhedronObject(RhinoSceneObject, GeometryObject):
    """Sceneobject for drawing polyhedron shapes.

    Parameters
    ----------
    polyhedron : :class:`~compas.geometry.Polyhedron`
        A COMPAS polyhedron.
    **kwargs : dict, optional
        Additional keyword arguments.

    """

    def __init__(self, polyhedron, **kwargs):
        super(PolyhedronObject, self).__init__(geometry=polyhedron, **kwargs)

    def draw(self, color=None):
        """Draw the polyhedron associated with the sceneobject.

        Parameters
        ----------
        color : rgb1 | rgb255 | :class:`~compas.colors.Color`, optional
            The RGB color of the polyhedron.

        Returns
        -------
        System.Guid
            The GUID of the object created in Rhino.

        """
        color = Color.coerce(color) or self.color
        attr = attributes(name=self.geometry.name, color=color, layer=self.layer)

        vertices = [list(vertex) for vertex in self.geometry.vertices]
        faces = self.geometry.faces
        geometry = vertices_and_faces_to_rhino(vertices, faces)
        if self.transformation:
            geometry.Transform(transformation_to_rhino(self.transformation))

        return sc.doc.Objects.AddMesh(geometry, attr)
