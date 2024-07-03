from typing import Optional

import bpy  # type: ignore

from compas.colors import Color
from compas.scene import GeometryObject
from compas_blender import conversions

from .sceneobject import BlenderSceneObject


class CurveObject(BlenderSceneObject, GeometryObject):
    """Scene object for drawing curves in Blender."""

    def draw(
        self,
        color: Optional[Color] = None,
        collection: Optional[str] = None,
    ) -> list[bpy.types.Object]:
        """Draw the curve.

        Parameters
        ----------
        color : tuple[int, int, int] | tuple[float, float, float] | :class:`compas.colors.Color`, optional
            The RGB color of the curve.
        collection : str, optional
            The name of the Blender scene collection containing the created object(s).

        Returns
        -------
        list[:blender:`bpy.types.Object`]
            The objects created in Blender.

        """
        name = self.geometry.name
        color = Color.coerce(color) or self.color
        # TODO: add support for NurbsCurve
        curve = conversions.polyline_to_blender_curve(self.geometry.to_polyline(), name=name)

        obj = self.create_object(curve, name=name)
        self.update_object(obj, color=color, collection=collection)

        self._guids = [obj]
        return self.guids
