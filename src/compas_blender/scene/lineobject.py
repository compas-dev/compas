from typing import Optional

import bpy  # type: ignore

from compas.colors import Color
from compas.scene import GeometryObject
from compas_blender import conversions

from .sceneobject import BlenderSceneObject


class LineObject(BlenderSceneObject, GeometryObject):
    """Scene object for drawing lines in Blender."""

    def draw(
        self,
        color: Optional[Color] = None,
        collection: Optional[str] = None,
    ) -> list[bpy.types.Object]:
        """Draw the line.

        Parameters
        ----------
        color : tuple[int, int, int] | tuple[float, float, float] | :class:`compas.colors.Color`, optional
            The RGB color of the box.
        collection : str, optional
            The name of the Blender scene collection containing the created object(s).

        Returns
        -------
        list[:blender:`bpy.types.Object`]
            The objects created in Blender.

        """
        name = self.geometry.name
        color = Color.coerce(color) or self.color

        curve = conversions.line_to_blender_curve(self.geometry)

        obj = self.create_object(curve, name=name)
        self.update_object(obj, color=color, collection=collection, show_wire=True)

        self._guids = [obj]
        return self.guids
