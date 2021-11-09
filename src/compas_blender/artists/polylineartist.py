from typing import Any
from typing import List
from typing import Optional
from typing import Union

import bpy

import compas_blender
from compas.artists import PrimitiveArtist
from compas.geometry import Polyline
from compas.utilities import RGBColor
from compas_blender.artists import BlenderArtist


class PolylineArtist(BlenderArtist, PrimitiveArtist):
    """Artist for drawing polylines.

    Parameters
    ----------
    polyline : :class:`compas.geometry.Polyline`
        A COMPAS polyline.
    collection: str or :class:`bpy.types.Collection`
        The name of the collection the object belongs to.
    """

    def __init__(self,
                 polyline: Polyline,
                 collection: Optional[Union[str, bpy.types.Collection]] = None,
                 **kwargs: Any
                 ):
        super().__init__(primitive=polyline, collection=collection or polyline.name, **kwargs)

    def draw(self, color: Optional[RGBColor] = None, show_points: Optional[bool] = False) -> List[bpy.types.Object]:
        """Draw the line.

        Parameters
        ----------
        color : tuple of float or tuple of int, optional
            The RGB color of the polyline.
        show_points : bool, optional
            Show the points of the polyline.
            Default is ``False``.

        Returns
        -------
        list of bpy.types.Object

        """
        color = color or self.color
        _points = map(list, self.primitive.points)

        lines = [
            {'start': start, 'end': end, 'color': self.color, 'name': f"{self.primitive.name}"}
            for start, end in self.primitive.lines
        ]
        objects = compas_blender.draw_lines(lines, collection=self.collection)

        if show_points:
            points = [
                {'pos': point, 'name': f"{self.primitive.name}.point", 'color': color, 'radius': 0.01}
                for point in _points
            ]
            objects += compas_blender.draw_points(points, collection=self.collection)
        return objects
