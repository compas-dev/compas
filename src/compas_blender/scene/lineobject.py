from typing import Any
from typing import List
from typing import Optional

import bpy  # type: ignore

from compas.geometry import Line
from compas.colors import Color

from compas_blender import conversions

from compas.scene import GeometryObject
from .sceneobject import BlenderSceneObject


class LineObject(BlenderSceneObject, GeometryObject):
    """Scene object for drawing lines in Blender.

    Parameters
    ----------
    line : :class:`compas.geometry.Line`
        A COMPAS line.
    **kwargs : dict, optional
        Additional keyword arguments.
        For more info,
        see :class:`compas_blender.scene.BlenderSceneObject` and :class:`compas.scene.GeometryObject`.

    """

    def __init__(self, line: Line, **kwargs: Any):
        super().__init__(geometry=line, **kwargs)

    def draw(
        self,
        color: Optional[Color] = None,
        collection: Optional[str] = None,
    ) -> List[bpy.types.Object]:
        """Draw the line.

        Parameters
        ----------
        color : tuple[int, int, int] | tuple[float, float, float] | :class:`compas.colors.Color`, optional
            The RGB color of the box.
        collection : str, optional
            The name of the Blender scene collection containing the created object(s).

        Returns
        -------
        :blender:`bpy.types.Object`

        """
        name = self.geometry.name
        color = Color.coerce(color) or self.color

        curve = conversions.line_to_blender_curve(self.geometry)

        obj = self.create_object(curve, name=name)
        self.update_object(obj, color=color, collection=collection, show_wire=True)

        return obj
