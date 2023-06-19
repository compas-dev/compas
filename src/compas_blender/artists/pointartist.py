from typing import Any
from typing import List
from typing import Optional
from typing import Union

import bpy

import compas_blender
from compas.artists import PrimitiveArtist
from compas.geometry import Point
from compas.colors import Color
from .artist import BlenderArtist


class PointArtist(BlenderArtist, PrimitiveArtist):
    """Artist for drawing points in Blender.

    Parameters
    ----------
    point : :class:`~compas.geometry.Point`
        A COMPAS point.
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

        from compas.geometry import Point
        from compas_blender.artists import PointArtist

        point = Point(0, 0, 0)

        artist = PointArtist(point)
        artist.draw()

    Or, use the artist through the plugin mechanism.

    .. code-block:: python

        from compas.geometry import Point
        from compas.artists import Artist

        point = Point(0, 0, 0)

        artist = Artist(point)
        artist.draw()

    """

    def __init__(
        self,
        point: Point,
        collection: Optional[Union[str, bpy.types.Collection]] = None,
        **kwargs: Any,
    ):
        super().__init__(primitive=point, collection=collection or point.name, **kwargs)

    def draw(self, color: Optional[Color] = None) -> List[bpy.types.Object]:
        """Draw the point.

        Parameters
        ----------
        color : tuple[float, float, float] | tuple[int, int, int] | :class:`~compas.colors.Color`, optional
            Color of the point object.
            The default color is :attr:`compas.artists.PrimitiveArtist.color`.

        Returns
        -------
        list[:blender:`bpy.types.Object`]

        """
        color = Color.coerce(color) or self.color
        points = [
            {
                "pos": self.primitive,
                "name": f"{self.primitive.name}",
                "color": color,
                "radius": 0.01,
            }
        ]
        objects = compas_blender.draw_points(points, self.collection)
        return objects
