from typing import Any
from typing import List
from typing import Optional
from typing import Union

import bpy  # type: ignore

from compas.artists import GeometryArtist
from compas.geometry import Line
from compas.colors import Color
from compas_blender.artists import BlenderArtist

from compas_blender.conversions import line_to_blender_curve


class LineArtist(BlenderArtist, GeometryArtist):
    """Artist for drawing lines in Blender.

    Parameters
    ----------
    line : :class:`~compas.geometry.Line`
        A COMPAS line.
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

        from compas.geometry import Line
        from compas_blender.artists import LineArtist

        line = Line([0, 0, 0], [1, 1, 1])

        artist = LineArtist(line)
        artist.draw()

    Or, use the artist through the plugin mechanism.

    .. code-block:: python

        from compas.geometry import Line
        from compas.artists import Artist

        line = Line([0, 0, 0], [1, 1, 1])

        artist = Artist(line)
        artist.draw()

    """

    def __init__(
        self,
        line: Line,
        collection: Optional[Union[str, bpy.types.Collection]] = None,
        **kwargs: Any,
    ):
        super().__init__(
            geometry=line,
            collection=collection or line.name,
            **kwargs,
        )

    def draw(
        self,
        color: Optional[Color] = None,
        show_points: bool = False,
    ) -> List[bpy.types.Object]:
        """Draw the line.

        Parameters
        ----------
        color : tuple[int, int, int] | tuple[float, float, float] | :class:`~compas.colors.Color`, optional
            The RGB color of the box.
            The default color is :attr:`compas.artists.GeometryArtist.color`.
        show_points : bool, optional
            If True, show the start and end point in addition to the line.

        Returns
        -------
        list[:blender:`bpy.types.Object`]

        """
        color = Color.coerce(color) or self.color

        curve = line_to_blender_curve(self.geometry)
        obj = bpy.data.objects.new(self.geometry.name, curve)

        self.link_object(obj)
        if color:
            self.assign_object_color(obj, color)

        return obj
