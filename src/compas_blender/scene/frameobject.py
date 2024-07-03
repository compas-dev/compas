from typing import Any
from typing import Optional

import bpy  # type: ignore

from compas.colors import Color
from compas.geometry import Line
from compas.scene import GeometryObject
from compas_blender import conversions

from .sceneobject import BlenderSceneObject


class FrameObject(BlenderSceneObject, GeometryObject):
    """Scene object for drawing frames in Blender.

    Parameters
    ----------
    scale : float, optional
        Scale of the frame axes.
    **kwargs : dict, optional
        Additional keyword arguments.
        For more info,
        see :class:`compas_blender.scene.BlenderSceneObject` and :class:`compas.scene.GeometryObject`.

    Attributes
    ----------
    color_origin : :class:`compas.colors.Color`
        Color for the point at the frame origin.
        Default is ``Color.black()``.
    color_xaxis : :class:`compas.colors.Color`
        Default is ``Color.red()``.
    color_yaxis : :class:`compas.colors.Color`
        Default is ``Color.green()``.
    color_zaxis : :class:`compas.colors.Color`
        Default is ``Color.blue()``.

    """

    def __init__(self, scale=1.0, **kwargs: Any):
        super().__init__(**kwargs)
        self.scale = scale
        self.color_origin = Color.black()
        self.color_xaxis = Color.red()
        self.color_yaxis = Color.green()
        self.color_zaxis = Color.blue()

    def draw(
        self,
        collection: Optional[str] = None,
    ) -> list[bpy.types.Object]:
        """Draw the frame.

        Parameters
        ----------
        collection : str, optional
            The Blender scene collection containing the created objects.

        Returns
        -------
        list[:blender:`bpy.types.Object`]
            The objects created in Blender.
        """
        objects = []

        name = self.geometry.name
        collection = collection or name

        origin = self.geometry.point
        X = self.geometry.point + self.geometry.xaxis.scaled(self.scale)
        Y = self.geometry.point + self.geometry.yaxis.scaled(self.scale)
        Z = self.geometry.point + self.geometry.zaxis.scaled(self.scale)

        lines = [
            {
                "start": origin,
                "end": X,
                "color": self.color_xaxis,
                "name": f"{self.geometry.name}.xaxis",
            },
            {
                "start": origin,
                "end": Y,
                "color": self.color_yaxis,
                "name": f"{self.geometry.name}.yaxis",
            },
            {
                "start": origin,
                "end": Z,
                "color": self.color_zaxis,
                "name": f"{self.geometry.name}.zaxis",
            },
        ]

        for line in lines:
            curve = conversions.line_to_blender_curve(Line(line["start"], line["end"]))
            obj = self.create_object(curve, name=line["name"])
            self.update_object(obj, color=line["color"], collection=collection, show_wire=True)
            objects.append(obj)

        self._guids = objects
        return self.guids
