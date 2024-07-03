from typing import Optional

import bpy  # type: ignore

from compas.colors import Color
from compas.geometry import Line
from compas.geometry import Point
from compas.scene import GeometryObject
from compas_blender import conversions

from .sceneobject import BlenderSceneObject


class VectorObject(BlenderSceneObject, GeometryObject):
    """Scene object for drawing vectors in Blender."""

    def draw(
        self,
        color: Optional[Color] = None,
        collection: Optional[str] = None,
        point: Optional[Point] = None,
    ) -> list[bpy.types.Object]:
        """Draw the vector.

        Parameters
        ----------
        color : tuple[float, float, float] | tuple[int, int, int] | :class:`compas.colors.Color`, optional
            The RGB color of the vector.
        collection : str, optional
            The name of the Blender scene collection containing the created object(s).
        point : [float, float, float] | :class:`compas.geometry.Point`, optional
            Point of application of the vector.
            Default is ``Point(0, 0, 0)``.

        Returns
        -------
        list[:blender:`bpy.types.Object`]
            The objects created in Blender.

        """
        name = self.geometry.name
        color = Color.coerce(color) or self.color

        point = point or (0.0, 0.0, 0.0)  # type: ignore
        start = Point(*point)  # type: ignore
        end = start + self.geometry
        line = Line(start, end)

        curve = conversions.line_to_blender_curve(line)

        obj = self.create_object(curve, name=name)
        self.update_object(obj, color=color, collection=collection)

        self._guids = [obj]
        return self.guids
