from typing import Any
from typing import List
from typing import Optional
from typing import Union

import bpy

import compas_blender
from compas.artists import PrimitiveArtist
from compas.geometry import Polyline
from compas.colors import Color
from .artist import BlenderArtist


class PolylineArtist(BlenderArtist, PrimitiveArtist):
    """Artist for drawing polylines in Blender.

    Parameters
    ----------
    polyline : :class:`~compas.geometry.Polyline`
        A COMPAS polyline.
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

        from compas.geometry import Polyline
        from compas_blender.artists import PolylineArtist

        polyline = Polyline([[0, 0, 0], [1, 0, 0], [1, 1, 0], [1, 1, 1]])

        artist = PolylineArtist(polyline)
        artist.draw()

    Or, use the artist through the plugin mechanism.

    .. code-block:: python

        from compas.geometry import Polyline
        from compas.artists import Artist

        polyline = Polyline([[0, 0, 0], [1, 0, 0], [1, 1, 0], [1, 1, 1]])

        artist = Artist(polyline)
        artist.draw()

    """

    def __init__(
        self,
        polyline: Polyline,
        collection: Optional[Union[str, bpy.types.Collection]] = None,
        **kwargs: Any,
    ):
        super().__init__(primitive=polyline, collection=collection or polyline.name, **kwargs)

    def draw(self, color: Optional[Color] = None, show_points: Optional[bool] = False) -> List[bpy.types.Object]:
        """Draw the line.

        Parameters
        ----------
        color : tuple[float, float, float] | tuple[int, int, int] | :class:`~compas.colors.Color`, optional
            The RGB color of the polyline.
            The default color is :attr:`compas.artists.PrimitiveArtist.color`.
        show_points : bool, optional
            If True, draw the corner points of the polyline.

        Returns
        -------
        list[:blender:`bpy.types.Object`]

        """
        color = Color.coerce(color) or self.color

        lines = [
            {
                "start": start,
                "end": end,
                "color": self.color,
                "name": f"{self.primitive.name}",
            }
            for start, end in self.primitive.lines
        ]
        objects = compas_blender.draw_lines(lines, collection=self.collection)

        if show_points:
            points = [
                {
                    "pos": point,
                    "name": f"{self.primitive.name}.point",
                    "color": color,
                    "radius": 0.01,
                }
                for point in self.primitive.points
            ]
            objects += compas_blender.draw_points(points, collection=self.collection)
        return objects
