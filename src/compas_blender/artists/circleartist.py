from typing import Any
from typing import List
from typing import Optional
from typing import Union

import bpy

import compas_blender
from compas.geometry import add_vectors
from compas.geometry import Circle
from compas.artists import PrimitiveArtist
from compas.utilities import RGBColor
from .artist import BlenderArtist


class CircleArtist(BlenderArtist, PrimitiveArtist):
    """Artist for drawing circles.

    Parameters
    ----------
    circle : :class:`compas.geometry.Circle`
        A COMPAS circle.
    collection :  str or :class:`bpy.types.Collection`
        The name of the collection the object belongs to.
    """

    def __init__(self,
                 circle: Circle,
                 collection: Optional[Union[str, bpy.types.Collection]] = None,
                 **kwargs: Any):
        super().__init__(primitive=circle, collection=collection or circle.name, **kwargs)

    def draw(self,  color: RGBColor = None, show_point=False, show_normal=False) -> List[bpy.types.Object]:
        """Draw the circle.

        Parameters
        ----------
        color : tuple of float or tuple of int, optional
            The RGB color of the capsule.
        show_point : bool, optional
            Default is ``False``.
        show_normal : bool, optional
            Default is ``False``.

        Returns
        -------
        list
            The objects created in Blender.
        """
        color = color or self.color
        point = list(self.primitive.plane.point)
        normal = list(self.primitive.plane.normal)
        plane = point, normal
        radius = self.primitive.radius
        objects = []
        if show_point:
            points = [{'pos': point, 'color': color, 'name': self.primitive.name, 'radius': 0.01}]
            objects += compas_blender.draw_points(points, collection=self.collection)
        if show_normal:
            end = add_vectors(point, normal)
            lines = [{'start': point, 'end': end, 'color': color, 'name': self.primitive.name}]
            objects += compas_blender.draw_lines(lines, collection=self.collection)
        circles = [{'plane': plane, 'radius': radius, 'color': color, 'name': self.primitive.name}]
        objects += compas_blender.draw_circles(circles, collection=self.collection)
        return objects
