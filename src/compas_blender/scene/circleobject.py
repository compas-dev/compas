from typing import Any
from typing import Optional

import bpy  # type: ignore

from compas.geometry import Circle
from compas.colors import Color

from compas.scene import GeometryObject
from .sceneobject import BlenderSceneObject


class CircleObject(BlenderSceneObject, GeometryObject):
    """Scene object for drawing circles in Blender.

    Parameters
    ----------
    circle : :class:`compas.geometry.Circle`
        A COMPAS circle.
    **kwargs : dict, optional
        Additional keyword arguments.

    """

    def __init__(self, circle: Circle, **kwargs: Any):
        super().__init__(geometry=circle, **kwargs)

    def draw(self, color: Optional[Color] = None, collection: Optional[str] = None) -> bpy.types.Object:
        """Draw the circle.

        Parameters
        ----------
        color : tuple[int, int, int] | tuple[float, float, float] | :class:`compas.colors.Color`, optional
            The RGB color of the capsule.
        collection : str, optional
            The name of the Blender scene collection containing the created object(s).

        Returns
        -------
        :blender:`bpy.types.Object`
            The object created in Blender.

        """
        color = Color.coerce(color) or self.color

        bpy.ops.curve.primitive_bezier_circle_add(radius=self.geometry.radius)

        obj = bpy.context.object
        self.objects.append(obj)
        self.update_object(obj, color=color, collection=collection, transformation=self.geometry.transformation)

        return obj
