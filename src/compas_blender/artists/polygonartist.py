from typing import Any
from typing import List
from typing import Optional
from typing import Union

import bpy

import compas_blender
from compas.artists import PrimitiveArtist
from compas.geometry import Polygon
from compas.utilities import RGBColor
from compas_blender.artists import BlenderArtist


class PolygonArtist(BlenderArtist, PrimitiveArtist):
    """Artist for drawing polygons.

    Parameters
    ----------
    polygon : :class:`compas.geometry.Polygon`
        A COMPAS polygon.
    collection : str or :class:`bpy.types.Collection`
        The name of the collection the object belongs to.
    """

    def __init__(self,
                 polygon: Polygon,
                 collection: Optional[Union[str, bpy.types.Collection]] = None,
                 **kwargs: Any):
        super().__init__(primitive=polygon, collection=collection or polygon.name, **kwargs)

    def draw(self,
             color: RGBColor = None,
             show_points=False,
             show_edges=False,
             show_face=True) -> List[bpy.types.Object]:
        """Draw the polygon.

        Parameters
        ----------
        color : tuple of float or tuple of int, optional
            The RGB color of the polygon.
        show_points : bool, optional
            Default is ``False``.
        show_edges : bool, optional
            Default is ``False``.
        show_face : bool, optional
            Default is ``True``.

        Returns
        -------
        list of bpy.types.Object
        """
        _points = map(list, self.primitive.points)
        color = color or self.color
        objects = []
        if show_points:
            points = [{'pos': point, 'color': color, 'name': self.primitive.name, 'radius': 0.01} for point in _points]
            objects += compas_blender.draw_points(points, collection=self.collection)
        if show_edges:
            lines = [{'start': list(a), 'end': list(b), 'color': color, 'name': self.primitive.name} for a, b in self.primitive.lines]
            objects += compas_blender.draw_lines(lines, collection=self.collection)
        if show_face:
            polygons = [{'points': list(_points), 'color': color, 'name': self.primitive.name}]
            objects += compas_blender.draw_faces(polygons, collection=self.collection)
        return objects
