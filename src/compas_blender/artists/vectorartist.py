from typing import Any
from typing import List
from typing import Optional
from typing import Union

import bpy

import compas_blender
from compas.artists import PrimitiveArtist
from compas.geometry import Point
from compas.geometry import Vector
from compas.utilities import RGBColor
from compas_blender.artists import BlenderArtist


__all__ = ['VectorArtist']


class VectorArtist(BlenderArtist, PrimitiveArtist):
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

    def __init__(self,
                 vector: Vector,
                 collection: Optional[Union[str, bpy.types.Collection]] = None,
                 **kwargs: Any):
        super().__init__(primitive=vector, collection=collection or vector.name, **kwargs)

    def draw(self,
             color: Optional[RGBColor] = None,
             point: Optional[Point] = None,
             show_point: Optional[bool] = False) -> List[bpy.types.Object]:
        """Draw the vector.

        Parameters
        ----------
        color : tuple of float or tuple of int, optional
            The RGB color of the vector.
        point : [float, float, float] or :class:`compas.geometry.Point`, optional
            Point of application of the vector.
            Default is ``Point(0, 0, 0)``.
        show_point : bool, optional
            Show the point of application of the vector.
            Default is ``False``.

        Returns
        -------
        list of :class:`bpy.types.Object`
        """
        start = point or (0., 0., 0.)
        end = tuple(map(sum, zip(start, self.primitive)))
        color = color or self. color
        lines = [
            {'start': start, 'end': end, 'color': color, 'name': f"{self.primitive.name}"},
        ]
        objects = compas_blender.draw_lines(lines, self.collection)
        if show_point:
            points = [{
                'pos': start,
                'name': f"{self.primitive.name}.origin",
                'color': (1.0, 1.0, 1.0),
                'radius': 0.01,
            }]
            objects += compas_blender.draw_points(points, self.collection)
        return objects
