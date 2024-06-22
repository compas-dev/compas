from typing import Optional

import bpy  # type: ignore

from compas.colors import Color
from compas.scene import GeometryObject

from .sceneobject import BlenderSceneObject


class PointObject(BlenderSceneObject, GeometryObject):
    """Scene object for drawing points in Blender."""

    def draw(
        self,
        color: Optional[Color] = None,
        collection: Optional[str] = None,
        radius: float = 0.01,
        u: int = 16,
        v: int = 16,
    ) -> list[bpy.types.Object]:
        """Draw the point.

        Parameters
        ----------
        color : tuple[float, float, float] | tuple[int, int, int] | :class:`compas.colors.Color`, optional
            Color of the point object.
        collection : str, optional
            The name of the Blender scene collection containing the created object(s).
        radius : float, optional
            Radius of the point object.
        u : int, optional
            Number of faces in the "u" direction.
        v : int, optional
            Number of faces in the "v" direction.

        Returns
        -------
        list[:blender:`bpy.types.Object`]

        """
        name = self.geometry.name
        color = Color.coerce(color) or self.color

        bpy.ops.mesh.primitive_uv_sphere_add(
            location=self.geometry,
            radius=radius,
            segments=u,
            ring_count=v,
        )

        obj = bpy.context.object
        self.objects.append(obj)
        self.update_object(obj, name=name, color=color, collection=collection)

        self._guids = [obj]
        return self.guids
