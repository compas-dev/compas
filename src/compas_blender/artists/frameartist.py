from typing import Any
from typing import List
from typing import Optional
from typing import Union

import bpy

from compas.geometry import Frame

import compas_blender
from compas.artists import PrimitiveArtist
from compas.colors import Color
from .artist import BlenderArtist


class FrameArtist(BlenderArtist, PrimitiveArtist):
    """Artist for drawing frames in Blender.

    Parameters
    ----------
    frame: :class:`~compas.geometry.Frame`
        A COMPAS frame.
    collection : str | :blender:`bpy.types.Collection`
        The Blender scene collection the object(s) created by this artist belong to.
    scale: float, optional
        Scale factor that controls the length of the axes.
    **kwargs : dict, optional
        Additional keyword arguments.
        For more info,
        see :class:`~compas_blender.artists.BlenderArtist` and :class:`~compas.artists.PrimitiveArtist`.

    Attributes
    ----------
    scale : float
        Scale factor that controls the length of the axes.
        Default is ``1.0``.
    color_origin : :class:`~compas.colors.Color`
        Color for the point at the frame origin.
        Default is ``Color.black()``.
    color_xaxis : :class:`~compas.colors.Color`
        Default is ``Color.red()``.
    color_yaxis : :class:`~compas.colors.Color`
        Default is ``Color.green()``.
    color_zaxis : :class:`~compas.colors.Color`
        Default is ``Color.blue()``.

    """

    def __init__(
        self,
        frame: Frame,
        collection: Optional[Union[str, bpy.types.Collection]] = None,
        scale: float = 1.0,
        **kwargs: Any,
    ):

        super().__init__(primitive=frame, collection=collection or frame.name, **kwargs)

        self.scale = scale or 1.0
        self.color_origin = Color.black()
        self.color_xaxis = Color.red()
        self.color_yaxis = Color.green()
        self.color_zaxis = Color.blue()

    def draw(self) -> List[bpy.types.Object]:
        """Draw the frame.

        Returns
        -------
        list[:blender:`bpy.types.Object`]

        """
        self.clear()
        objects = []
        objects += self.draw_origin()
        objects += self.draw_axes()
        return objects

    def draw_origin(self) -> List[bpy.types.Object]:
        """Draw the origin of the frame.

        Returns
        -------
        list[:blender:`bpy.types.Object`]

        """
        points = [
            {
                "pos": self.primitive.point,
                "name": f"{self.primitive.name}.origin",
                "color": self.color_origin,
                "radius": 0.01,
            }
        ]
        return compas_blender.draw_points(points, self.collection)

    def draw_axes(self) -> List[bpy.types.Object]:
        """Draw the axes of the frame.

        Returns
        -------
        list[:blender:`bpy.types.Object`]

        """
        origin = self.primitive.point
        X = self.primitive.point + self.primitive.xaxis.scaled(self.scale)
        Y = self.primitive.point + self.primitive.yaxis.scaled(self.scale)
        Z = self.primitive.point + self.primitive.zaxis.scaled(self.scale)
        lines = [
            {
                "start": origin,
                "end": X,
                "color": self.color_xaxis,
                "name": f"{self.primitive.name}.xaxis",
            },
            {
                "start": origin,
                "end": Y,
                "color": self.color_yaxis,
                "name": f"{self.primitive.name}.yaxis",
            },
            {
                "start": origin,
                "end": Z,
                "color": self.color_zaxis,
                "name": f"{self.primitive.name}.zaxis",
            },
        ]
        return compas_blender.draw_lines(lines, self.collection)
