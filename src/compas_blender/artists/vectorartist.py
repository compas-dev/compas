from typing import List
from typing import Optional

import bpy

from compas.geometry import Point
import compas_blender
from compas_blender.artists._primitiveartist import PrimitiveArtist


__all__ = ['VectorArtist']


class VectorArtist(PrimitiveArtist):
    """Artist for drawing vectors.

    Parameters
    ----------
    primitive : :class:`compas.geometry.Vector`
        A COMPAS vector.

    Notes
    -----
    See :class:`compas_blender.artists.PrimitiveArtist` for all other parameters.

    Examples
    --------
    .. code-block:: python

        import random
        from compas.geometry import Pointcloud
        from compas.geometry import Vector
        from compas.utilities import i_to_rgb
\
        from compas_blender.artists import VectorArtist

        pcl = Pointcloud.from_bounds(10, 10, 10, 100)

        for point in pcl.points:
            vector = Vector(0, 0, 1)
            artist = VectorArtist(vector, color=i_to_rgb(random.random()))
            artist.draw(point=point)

    """
    def draw(self, point: Optional[Point] = None, show_point: Optional[bool] = False) -> List[bpy.types.Object]:
        """Draw the vector.

        Parameters
        ----------
        point : [float, float, float] or :class:`compas.geometry.Point`, optional
            Point of application of the vector.
            Default is ``Point(0, 0, 0)``.
        show_point : bool, optional
            Show the point of application of the vector.
            Default is ``False``.

        Returns
        -------
        list of bpy.types.Object

        """
        """Draw the axes of the frame.

        Returns
        -------
        list of :class:`bpy.types.Object`
        """
        start = point or (0., 0., 0.)
        end = tuple(map(sum, zip(start, self.primitive)))
        lines = [
            {'start': start, 'end': end, 'color': self.color, 'name': f"{self.primitive.name}"},
        ]
        objects = compas_blender.draw_lines(lines, self.collection)
        self.objects += objects
        return objects
