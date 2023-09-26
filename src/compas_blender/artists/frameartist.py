from typing import Any
from typing import List
from typing import Optional

import bpy  # type: ignore

from compas.geometry import Frame
from compas.colors import Color

from compas.artists import GeometryArtist
from .artist import BlenderArtist


class FrameArtist(BlenderArtist, GeometryArtist):
    """Artist for drawing frames in Blender.

    Parameters
    ----------
    frame: :class:`~compas.geometry.Frame`
        A COMPAS frame.
    **kwargs : dict, optional
        Additional keyword arguments.
        For more info,
        see :class:`~compas_blender.artists.BlenderArtist` and :class:`~compas.artists.GeometryArtist`.

    Attributes
    ----------
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

    def __init__(self, frame: Frame, **kwargs: Any):
        super().__init__(geometry=frame, **kwargs)
        self.color_origin = Color.black()
        self.color_xaxis = Color.red()
        self.color_yaxis = Color.green()
        self.color_zaxis = Color.blue()

    def draw(
        self,
        scale=1.0,
        collection: Optional[str] = None,
    ) -> List[bpy.types.Object]:
        """Draw the frame.

        Parameters
        ----------
        scale : float, optional
            Scale of the frame axes.
        collection : str, optional
            The Blender scene collection containing the created objects.

        Returns
        -------
        list[:blender:`bpy.types.Object`]

        """
        objects = []

        name = self.geometry.name
        collection = collection or name

        bpy.ops.mesh.primitive_uv_sphere_add(
            location=self.geometry,
            radius=0.01,
            segments=16,
            ring_count=16,
        )
        obj = bpy.context.object
        objects.append(obj)

        self.update_object(obj, color=self.color_origin, collection=collection)

        # origin = self.geometry.point
        # X = self.geometry.point + self.geometry.xaxis.scaled(self.scale)
        # Y = self.geometry.point + self.geometry.yaxis.scaled(self.scale)
        # Z = self.geometry.point + self.geometry.zaxis.scaled(self.scale)
        # lines = [
        #     {
        #         "start": origin,
        #         "end": X,
        #         "color": self.color_xaxis,
        #         "name": f"{self.geometry.name}.xaxis",
        #     },
        #     {
        #         "start": origin,
        #         "end": Y,
        #         "color": self.color_yaxis,
        #         "name": f"{self.geometry.name}.yaxis",
        #     },
        #     {
        #         "start": origin,
        #         "end": Z,
        #         "color": self.color_zaxis,
        #         "name": f"{self.geometry.name}.zaxis",
        #     },
        # ]
        # return compas_blender.draw_lines(lines, self.collection)

        return objects
