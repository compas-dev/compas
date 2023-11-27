from typing import Any
from typing import List
from typing import Optional

import bpy  # type: ignore
from compas.geometry import Polyhedron
from compas.colors import Color

from compas.scene import GeometryObject
from .sceneobject import BlenderSceneObject

from compas_blender import conversions


class PolyhedronObject(BlenderSceneObject, GeometryObject):
    """Sceneobject for drawing polyhedron shapes in Blender.

    Parameters
    ----------
    polyhedron : :class:`compas.geometry.Polyhedron`
        A COMPAS polyhedron.
    **kwargs : dict, optional
        Additional keyword arguments.

    """

    def __init__(self, polyhedron: Polyhedron, **kwargs: Any):
        super().__init__(geometry=polyhedron, **kwargs)

    def draw(
        self, color: Optional[Color] = None, collection: Optional[str] = None, show_wire: bool = True
    ) -> List[bpy.types.Object]:
        """Draw the polyhedron associated with the sceneobject.

        Parameters
        ----------
        color : tuple[float, float, float] | tuple[int, int, int] | :class:`compas.colors.Color`, optional
            The RGB color of the polyhedron.
        collection : str, optional
            The name of the Blender scene collection containing the created object(s).
        show_wire : bool, optional
            Display the wireframe of the polyhedron.

        Returns
        -------
        :blender:`bpy.types.Object`
            The object created in Blender.

        """
        name = self.geometry.name
        color = Color.coerce(color) or self.color

        vertices, faces = self.geometry.to_vertices_and_faces()
        mesh = conversions.vertices_and_faces_to_blender_mesh(vertices, faces, name=self.geometry.name)

        obj = self.create_object(mesh, name=name)
        self.update_object(obj, color=color, collection=collection, show_wire=show_wire)

        return obj
