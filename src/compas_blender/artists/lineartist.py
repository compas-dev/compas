from typing import List
from typing import Optional

import bpy

import compas_blender
from compas_blender.artists._primitiveartist import PrimitiveArtist


__all__ = ['LineArtist']


class LineArtist(PrimitiveArtist):
    """Artist for drawing lines.

    Parameters
    ----------
    primitive : :class:`compas.geometry.Line`
        A COMPAS line.

    Notes
    -----
    See :class:`compas_blender.artists.PrimitiveArtist` for all other parameters.

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

    def draw(self, show_points: Optional[bool] = False) -> List[bpy.types.Object]:
        """Draw the line.

        Parameters
        ----------
        show_points : bool, optional
            Show the start and end point.
            Default is ``False``.

        Returns
        -------
        list of bpy.types.Object

        """
        start = list(self.primitive.start)
        end = list(self.primitive.end)
        objects = []
        if show_points:
            points = [
                {'pos': start, 'name': f"{self.name}.start", 'color': self.color, 'radius': 0.01},
                {'pos': end, 'name': f"{self.name}.end", 'color': self.color, 'radius': 0.01},
            ]
            objects += compas_blender.draw_points(points, collection=self.collection)
        lines = [
            {'start': start, 'end': end, 'color': self.color, 'name': f"{self.name}"},
        ]
        objects += compas_blender.draw_lines(lines, collection=self.collection)
        self.objects = objects
        return objects
