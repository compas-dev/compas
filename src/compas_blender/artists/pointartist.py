from typing import List

import bpy

import compas_blender
from compas_blender.artists import PrimitiveArtist


__all__ = ["PointArtist"]


class PointArtist(PrimitiveArtist):
    """Artist for drawing points.

    Parameters
    ----------
    primitive : :class:`compas.geometry.Point`
        A COMPAS point.

    Notes
    -----
    See :class:`compas_blender.artists.PrimitiveArtist` for all other parameters.

    Examples
    --------
    .. code-block:: python

        import random
        from compas.geometry import Pointcloud
        from compas.utilities import i_to_rgb

        import compas_blender
        from compas_blender.artists import PointArtist

        pcl = Pointcloud.from_bounds(10, 10, 10, 100)

        for point in pcl.points:
            artist = PointArtist(point, color=i_to_rgb(random.random()))
            artist.draw()

    """
    def draw(self) -> List[bpy.types.Object]:
        """Draw the point.

        Returns
        -------
        list of :class:`bpy.types.Object`
        """
        points = [{
                'pos': self.primitive,
                'name': f"{self.name}",
                'color': self.color,
                'radius': 0.01
            }]
        objects = compas_blender.draw_points(points, self.collection)
        self.objects += objects
        return objects

