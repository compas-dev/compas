from typing import Any
from typing import Optional

import bpy  # type: ignore

from compas.geometry import Polyline
from compas.colors import Color

from compas.scene import GeometryObject
from .sceneobject import BlenderSceneObject

from compas_blender import conversions


class PolylineObject(BlenderSceneObject, GeometryObject):
    """Scene object for drawing polylines in Blender.

    Parameters
    ----------
    polyline : :class:`compas.geometry.Polyline`
        A COMPAS polyline.
    **kwargs : dict, optional
        Additional keyword arguments.

    """

    def __init__(self, polyline: Polyline, **kwargs: Any):
        super().__init__(geometry=polyline, **kwargs)

    def draw(self, color: Optional[Color] = None, collection: Optional[str] = None) -> list[bpy.types.Object]:
        """Draw the line.

        Parameters
        ----------
        color : tuple[float, float, float] | tuple[int, int, int] | :class:`compas.colors.Color`, optional
            The RGB color of the polyline.
        collection : str, optional
            The name of the Blender scene collection containing the created object(s).

        Returns
        -------
        list[:blender:`bpy.types.Object`]
            The objects created in Blender.

        """
        name = self.geometry.name
        color = Color.coerce(color) or self.color

        curve = conversions.polyline_to_blender_curve(self.geometry, name=name)

        obj = self.create_object(curve, name=name)
        self.update_object(obj, color=color, collection=collection)

        self._guids = [obj]
        return self.guids
