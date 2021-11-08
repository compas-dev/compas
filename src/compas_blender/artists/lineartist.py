from typing import Any
from typing import List
from typing import Optional
from typing import Union

import bpy

import compas_blender
from compas.artists import PrimitiveArtist
from compas.geometry import Line
from compas.utilities import RGBColor
from compas_blender.artists import BlenderArtist


class LineArtist(BlenderArtist, PrimitiveArtist):
    """Artist for drawing lines.

    Parameters
    ----------
    line : :class:`compas.geometry.Line`
        A COMPAS line.
    collection: str or :class:`bpy.types.Collection`
        The name of the collection the object belongs to.

    Examples
    --------
    .. code-block:: python

        import random
        from compas.geometry import Pointcloud
        from compas.geometry import Vector
        from compas.geometry import Line
        from compas.utilities import i_to_rgb

        from compas_blender.artists import LineArtist

        pcl = Pointcloud.from_bounds(10, 10, 10, 100)

        for point in pcl.points:
            line = Line(point, point + Vector(1, 0, 0))
            artist = LineArtist(line, color=i_to_rgb(random.random()))
            artist.draw()

    """

    def __init__(self,
                 line: Line,
                 collection: Optional[Union[str, bpy.types.Collection]] = None,
                 **kwargs: Any
                 ):
        super().__init__(primitive=line, collection=collection or line.name, **kwargs)

    def draw(self, color: RGBColor = None, show_points: Optional[bool] = False) -> List[bpy.types.Object]:
        """Draw the line.

        Parameters
        ----------
        color : tuple of float or tuple of int, optional
            The RGB color of the box.
        show_points : bool, optional
            Show the start and end point.
            Default is ``False``.

        Returns
        -------
        list of bpy.types.Object

        """
        color = color or self.color
        start = list(self.primitive.start)
        end = list(self.primitive.end)
        objects = []
        if show_points:
            points = [
                {'pos': start, 'name': f"{self.primitive.name}.start", 'color': color, 'radius': 0.01},
                {'pos': end, 'name': f"{self.primitive.name}.end", 'color': color, 'radius': 0.01},
            ]
            objects += compas_blender.draw_points(points, collection=self.collection)
        lines = [
            {'start': start, 'end': end, 'color': color, 'name': f"{self.primitive.name}"},
        ]
        objects += compas_blender.draw_lines(lines, collection=self.collection)
        return objects
