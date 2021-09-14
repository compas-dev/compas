import bpy
from typing import List
from typing import Optional

from compas.geometry import Frame

import compas_blender
from compas_blender.artists import BaseArtist


__all__ = ['FrameArtist']


class FrameArtist(BaseArtist):
    """Artist for drawing frames.

    Parameters
    ----------
    frame: :class:`compas.geometry.Frame`
        A COMPAS frame.
    collection: str
        The name of the frame's collection.
    scale: float, optional
        Scale factor that controls the length of the axes.

    Attributes
    ----------
    frame: :class:`compas.geometry.Frame`
        A COMPAS frame.
    collection: str
        The name of the frame's collection.
    scale : float
        Scale factor that controls the length of the axes.
        Default is ``1.0``.
    color_origin : tuple of 3 int between 0 and 255
        Default is ``(0, 0, 0)``.
    color_xaxis : tuple of 3 int between 0 and 255
        Default is ``(255, 0, 0)``.
    color_yaxis : tuple of 3 int between 0 and 255
        Default is ``(0, 255, 0)``.
    color_zaxis : tuple of 3 int between 0 and 255
        Default is ``(0, 0, 255)``.

    Examples
    --------
    .. code-block:: python

        from compas.geometry import Pointcloud
        from compas.geometry import Frame

        from compas_blender.artists import FrameArtist

        pcl = Pointcloud.from_bounds(10, 10, 10, 100)
        tpl = Frame([0, 0, 0], [1, 0, 0], [0, 1, 0])


        for point in pcl.points:
            frame = tpl.copy()
            frame.point = point
            artist = FrameArtist(frame)
            artist.draw()

    """
    def __init__(self,
                 frame: Frame,
                 collection: Optional[bpy.types.Collection] = None,
                 scale: Optional[float] = 1.0):
        super(FrameArtist, self).__init__()
        self.collection = collection
        self.frame = frame
        self.scale = scale or 1.0
        self.color_origin = (0, 0, 0)
        self.color_xaxis = (255, 0, 0)
        self.color_yaxis = (0, 255, 0)
        self.color_zaxis = (0, 0, 255)

    def draw(self) -> None:
        """Draw the frame.

        Returns
        -------
        ``None``
        """
        self.clear()
        self.draw_origin()
        self.draw_axes()

    def draw_origin(self) -> List[bpy.types.Object]:
        """Draw the origin of the frame.

        Returns
        -------
        list of :class:`bpy.types.Object`
        """
        points = [{
                'pos': self.frame.point,
                'name': f"{self.frame.name}.origin",
                'color': self.color_origin,
                'radius': 0.01
            }]
        objects = compas_blender.draw_points(points, self.collection)
        self.objects += objects
        return objects

    def draw_axes(self) -> List[bpy.types.Object]:
        """Draw the axes of the frame.

        Returns
        -------
        list of :class:`bpy.types.Object`
        """
        origin = list(self.frame.point)
        X = list(self.frame.point + self.frame.xaxis.scaled(self.scale))
        Y = list(self.frame.point + self.frame.yaxis.scaled(self.scale))
        Z = list(self.frame.point + self.frame.zaxis.scaled(self.scale))
        lines = [
            {'start': origin, 'end': X, 'color': self.color_xaxis, 'name': f"{self.frame.name}.xaxis"},
            {'start': origin, 'end': Y, 'color': self.color_yaxis, 'name': f"{self.frame.name}.yaxis"},
            {'start': origin, 'end': Z, 'color': self.color_zaxis, 'name': f"{self.frame.name}.zaxis"},
        ]
        objects = compas_blender.draw_lines(lines, self.collection)
        self.objects += objects
        return objects
