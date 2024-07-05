from typing import Any
from typing import Optional

import bpy  # type: ignore

from compas.geometry import Shape
from compas.scene import GeometryObject
from compas_blender import conversions

from .sceneobject import BlenderSceneObject


class ShapeObject(BlenderSceneObject, GeometryObject):
    """Scene object for drawing capsule shapes in Blender.

    Parameters
    ----------
    v : int, optional
        The number of vertices in the u-direction of non-OCC geometries.
    u : int, optional
        The number of vertices in the v-direction of non-OCC geometries.
    **kwargs : dict, optional
        Additional keyword arguments.

    """

    def __init__(
        self,
        u: Optional[int] = 16,
        v: Optional[int] = 16,
        shade_smooth: bool = True,
        **kwargs: Any,
    ):
        super().__init__(**kwargs)
        self.geometry: Shape
        self.u = u
        self.v = v
        self.shade_smooth = shade_smooth

    @property
    def u(self) -> int:
        return self.geometry.resolution_u

    @u.setter
    def u(self, u: int) -> None:
        self.geometry.resolution_u = u

    @property
    def v(self) -> int:
        return self.geometry.resolution_v

    @v.setter
    def v(self, v: int) -> None:
        self.geometry.resolution_v = v

    def draw(self) -> list[bpy.types.Object]:
        """Draw the cone associated with the scene object.

        Returns
        -------
        list[:blender:`bpy.types.Object`]
            The objects created in Blender.

        """
        mesh = conversions.vertices_and_faces_to_blender_mesh(self.geometry.vertices, self.geometry.faces, name=self.geometry.name)
        if self.shade_smooth:
            mesh.shade_smooth()
        else:
            mesh.shade_flat()

        obj = self.create_object(mesh, name=self.geometry.name)
        self.update_object(obj, color=self.color, collection=self.collection, show_wire=self.show_wire)

        self._guids = [obj]
        return self.guids
