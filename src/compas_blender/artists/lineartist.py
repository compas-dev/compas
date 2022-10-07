from typing import Any
from typing import List
from typing import Optional
from typing import Union

import bpy

import compas_blender
from compas.artists import PrimitiveArtist
from compas.geometry import Line
from compas.colors import Color
from compas_blender.artists import BlenderArtist


class LineArtist(BlenderArtist, PrimitiveArtist):
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
        see :class:`~compas_blender.artists.BlenderArtist` and :class:`~compas.artists.PrimitiveArtist`.

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
        super().__init__(primitive=line, collection=collection or line.name, **kwargs)

    def draw(self, color: Optional[Color] = None, show_points: bool = False) -> List[bpy.types.Object]:
        """Draw the line.

        Parameters
        ----------
        color : tuple[int, int, int] | tuple[float, float, float] | :class:`~compas.colors.Color`, optional
            The RGB color of the box.
            The default color is :attr:`compas.artists.PrimitiveArtist.color`.
        show_points : bool, optional
            If True, show the start and end point in addition to the line.

        Returns
        -------
        list[:blender:`bpy.types.Object`]

        """
        color = Color.coerce(color) or self.color
        start = self.primitive.start
        end = self.primitive.end
        objects = []
        if show_points:
            points = [
                {
                    "pos": start,
                    "name": f"{self.primitive.name}.start",
                    "color": color,
                    "radius": 0.01,
                },
                {
                    "pos": end,
                    "name": f"{self.primitive.name}.end",
                    "color": color,
                    "radius": 0.01,
                },
            ]
            objects += compas_blender.draw_points(points, collection=self.collection)
        lines = [
            {
                "start": start,
                "end": end,
                "color": color,
                "name": f"{self.primitive.name}",
            },
        ]
        objects += compas_blender.draw_lines(lines, collection=self.collection)
        return objects
