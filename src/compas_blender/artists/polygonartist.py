from typing import Any
from typing import List
from typing import Optional
from typing import Union

import bpy

import compas_blender
from compas.artists import PrimitiveArtist
from compas.geometry import Polygon
from compas.colors import Color
from .artist import BlenderArtist


class PolygonArtist(BlenderArtist, PrimitiveArtist):
    """Artist for drawing polygons in Blender.

    Parameters
    ----------
    polygon : :class:`~compas.geometry.Polygon`
        A COMPAS polygon.
    collection : str | :blender:`bpy.types.Collection`
        The Blender scene collection the object(s) created by this artist belong to.
    **kwargs : dict, optional
        Additional keyword arguments.
        For more info,
        see :class:`~compas_blender.artists.BlenderArtist` and :class:`~compas.artists.PrimitiveArtist`.

    Examples
    --------
    .. code-block:: python

        from compas.geometry import Polygon
        from compas_blender.artists import PolygonArtist

        polygon = Polygon.from_sides_and_radius_xy(5, 1)

        artist = PolygonArtist(polygon)
        artist.draw()

    .. code-block:: python

        from compas.geometry import Polygon
        from compas.artists import Artist

        polygon = Polygon.from_sides_and_radius_xy(5, 1)

        artist = Artist(polygon)
        artist.draw()

    """

    def __init__(self, polygon: Polygon, collection: Optional[Union[str, bpy.types.Collection]] = None, **kwargs: Any):
        super().__init__(primitive=polygon, collection=collection or polygon.name, **kwargs)

    def draw(
        self,
        color: Optional[Color] = None,
        show_points: bool = False,
        show_edges: bool = False,
        show_face: bool = True,
    ) -> List[bpy.types.Object]:
        """Draw the polygon.

        Parameters
        ----------
        color : tuple[float, float, float] | tuple[int, int, int] | :class:`~compas.colors.Color`, optional
            The RGB color of the polygon.
            The default color is :attr:`compas.artists.PrimitiveArtist.color`.
        show_points : bool, optional
            If True, draw the corner points of the polygon.
        show_edges : bool, optional
            If True, draw the edges of the polygon.
        show_face : bool, optional
            If True, draw the face of the polygon.

        Returns
        -------
        list[:blender:`bpy.types.Object`]

        """
        color = Color.coerce(color) or self.color
        objects = []
        if show_points:
            points = [
                {
                    "pos": point,
                    "color": color,
                    "name": self.primitive.name,
                    "radius": 0.01,
                }
                for point in self.primitive.points
            ]
            objects += compas_blender.draw_points(points, collection=self.collection)
        if show_edges:
            lines = [
                {"start": a, "end": b, "color": color, "name": self.primitive.name} for a, b in self.primitive.lines
            ]
            objects += compas_blender.draw_lines(lines, collection=self.collection)
        if show_face:
            polygons = [
                {
                    "points": self.primitive.points,
                    "color": color,
                    "name": self.primitive.name,
                }
            ]
            objects += compas_blender.draw_faces(polygons, collection=self.collection)
        return objects
