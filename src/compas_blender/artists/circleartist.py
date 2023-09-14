from typing import Any
from typing import Optional
from typing import Union

import bpy  # type: ignore

from compas.geometry import Circle
from compas.artists import GeometryArtist
from compas.colors import Color
from .artist import BlenderArtist


class CircleArtist(BlenderArtist, GeometryArtist):
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
        see :class:`~compas_blender.artists.BlenderArtist` and :class:`~compas.artists.GeometryArtist`.

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

    def __init__(
        self,
        circle: Circle,
        collection: Optional[Union[str, bpy.types.Collection]] = None,
        **kwargs: Any,
    ):
        super().__init__(
            geometry=circle,
            collection=collection or circle.name,
            **kwargs,
        )

    def draw(
        self,
        color: Optional[Color] = None,
        show_point: bool = False,
        show_normal: bool = False,
    ) -> bpy.types.Object:
        """Draw the circle.

        Parameters
        ----------
        color : tuple[int, int, int] | tuple[float, float, float] | :class:`~compas.colors.Color`, optional
            The RGB color of the capsule.
            The default color is :attr:`compas.artists.GeometryArtist.color`.
        show_point : bool, optional
            If True, also draw the center point of the circle.
        show_normal : bool, optional
            If True, also draw the normal vector of the circle.

        Returns
        -------
        :blender:`bpy.types.Object`
            The object created in Blender.

        """
        color = Color.coerce(color) or self.color

        bpy.ops.curve.primitive_bezier_circle_add(radius=self.geometry.radius)

        obj = bpy.context.object
        obj.name = self.geometry.name
        obj.matrix_world = self.geometry.transformation.matrix

        self.link_object(obj)
        if color:
            self.assign_object_color(obj, color)

        return obj
