from typing import Any
from typing import Optional
from typing import Union

import bpy  # type: ignore

from compas.artists import GeometryArtist
from compas.geometry import Point
from compas.colors import Color
from .artist import BlenderArtist


class PointArtist(BlenderArtist, GeometryArtist):
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
        see :class:`~compas_blender.artists.BlenderArtist` and :class:`~compas.artists.GeometryArtist`.

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
        super().__init__(
            geometry=point,
            collection=collection or point.name,
            **kwargs,
        )

    def draw(
        self,
        color: Optional[Color] = None,
        size: float = 0.01,
        u: int = 16,
        v: int = 16,
    ) -> bpy.types.Object:
        """Draw the point.

        Parameters
        ----------
        color : tuple[float, float, float] | tuple[int, int, int] | :class:`~compas.colors.Color`, optional
            Color of the point object.
            The default color is :attr:`compas.artists.GeometryArtist.color`.

        Returns
        -------
        :blender:`bpy.types.Object`

        """
        color = Color.coerce(color) or self.color

        bpy.ops.mesh.primitive_uv_sphere_add(
            location=self.geometry,
            radius=size,
            segments=u,
            ring_count=v,
        )

        obj = bpy.context.object
        obj.name = self.geometry.name

        self.link_object(obj)
        if color:
            self.assign_object_color(obj, color)

        return obj
