from typing import Any

import bpy  # type: ignore

from compas.geometry import Box
from compas.scene import GeometryObject
from compas_blender import conversions

from .sceneobject import BlenderSceneObject


class BoxObject(BlenderSceneObject, GeometryObject):
    """Scene object for drawing box shapes in Blender.

    Parameters
    ----------
    box : :class:`compas.geometry.Box`
        A COMPAS box.
    **kwargs : dict, optional
        Additional keyword arguments.

    """

    def __init__(self, box: Box, **kwargs: Any):
        super().__init__(geometry=box, **kwargs)
        self.geometry: Box

    def draw(self) -> list[bpy.types.Object]:
        """Draw the box associated with the scene object.

        Returns
        -------
        list[:blender:`bpy.types.Object`]
            The object(s) created in Blender to represent the box.

        """
        mesh = conversions.vertices_and_faces_to_blender_mesh(self.geometry.vertices, self.geometry.faces, name=self.geometry.name)

        obj = self.create_object(mesh, name=self.geometry.name)
        self.update_object(obj, color=self.color, collection=self.collection, show_wire=self.show_wire)

        self._guids = [obj]
        return self.guids
