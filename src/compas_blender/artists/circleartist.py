from typing import Any
from typing import List
from typing import Optional
from typing import Union

import bpy

import compas_blender
from compas.geometry import add_vectors
from compas.geometry import Circle
from compas.artists import PrimitiveArtist
from compas.colors import Color
from .artist import BlenderArtist


class CircleArtist(BlenderArtist, PrimitiveArtist):
    """Artist for drawing circles in Blender.

    Parameters
    ----------
    circle : :class:`~compas.geometry.Circle`
        A COMPAS circle.
    collection : str | :blender:`bpy.types.Collection`
        The Blender scene collection the object(s) created by this artist belong to.
    **kwargs : dict, optional
        Additional keyword arguments.
        For more info,
        see :class:`~compas_blender.artists.BlenderArtist` and :class:`~compas.artists.PrimitiveArtist`.

    Examples
    --------
    Use the Blender artist explicitly.

    .. code-block:: python

        from compas.geometry import Plane, Circle
        from compas_blender.artists import CircleArtist

        circle = Circle(Plane([0, 0, 0], [0,, 0, 1]), 1.0)

        artist = CircleArtist(circle)
        artist.draw()

    Or, use the artist through the plugin mechanism.

    .. code-block:: python

        from compas.geometry import Plane, Circle
        from compas.artists import Artist

        circle = Circle(Plane([0, 0, 0], [0,, 0, 1]), 1.0)

        artist = Artist(circle)
        artist.draw()

    """

    def __init__(self, circle: Circle, collection: Optional[Union[str, bpy.types.Collection]] = None, **kwargs: Any):
        super().__init__(primitive=circle, collection=collection or circle.name, **kwargs)

    def draw(
        self,
        color: Optional[Color] = None,
        show_point: bool = False,
        show_normal: bool = False,
    ) -> List[bpy.types.Object]:
        """Draw the circle.

        Parameters
        ----------
        color : tuple[int, int, int] | tuple[float, float, float] | :class:`~compas.colors.Color`, optional
            The RGB color of the capsule.
            The default color is :attr:`compas.artists.PrimitiveArtist.color`.
        show_point : bool, optional
            If True, also draw the center point of the circle.
        show_normal : bool, optional
            If True, also draw the normal vector of the circle.

        Returns
        -------
        list[:blender:`bpy.types.Object`]
            The objects created in Blender.

        """
        color = Color.coerce(color) or self.color
        point = self.primitive.plane.point
        normal = self.primitive.plane.normal
        plane = point, normal
        radius = self.primitive.radius
        objects = []
        if show_point:
            points = [
                {
                    "pos": point,
                    "color": color,
                    "name": self.primitive.name,
                    "radius": 0.01,
                }
            ]
            objects += compas_blender.draw_points(points, collection=self.collection)
        if show_normal:
            end = add_vectors(point, normal)
            lines = [
                {
                    "start": point,
                    "end": end,
                    "color": color,
                    "name": self.primitive.name,
                }
            ]
            objects += compas_blender.draw_lines(lines, collection=self.collection)
        circles = [
            {
                "plane": plane,
                "radius": radius,
                "color": color,
                "name": self.primitive.name,
            }
        ]
        objects += compas_blender.draw_circles(circles, collection=self.collection)
        return objects
