from typing import Any
from typing import List
from typing import Optional
from typing import Union

import bpy

import compas_blender
from compas_blender.utilities import RGBColor
from compas.artists import PrimitiveArtist
from compas.geometry import Point
from compas_blender.artists import BlenderArtist


class PointArtist(BlenderArtist, PrimitiveArtist):
    """Artist for drawing points.

    Parameters
    ----------
    point : :class:`compas.geometry.Point`
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

        from compas_blender.artists import PointArtist

        pcl = Pointcloud.from_bounds(10, 10, 10, 100)

        for point in pcl.points:
            artist = PointArtist(point, color=i_to_rgb(random.random()))
            artist.draw()

    """

    def __init__(self,
                 point: Point,
                 collection: Optional[Union[str, bpy.types.Collection]] = None,
                 **kwargs: Any):
        super().__init__(primitive=point, collection=collection or point.name, **kwargs)

    def draw(self, color: Optional[RGBColor] = None) -> List[bpy.types.Object]:
        """Draw the point.

        Returns
        -------
        list of :class:`bpy.types.Object`
        """
        color = color or self.color
        points = [{
                'pos': self.primitive,
                'name': f"{self.primitive.name}",
                'color': color,
                'radius': 0.01
            }]
        objects = compas_blender.draw_points(points, self.collection)
        return objects
