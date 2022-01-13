from typing import Any
from typing import List
from typing import Optional
from typing import Union

import bpy

import compas_blender
from compas_blender.artists import BlenderArtist
from compas_blender.utilities import RGBColor
from compas.artists import PrimitiveArtist
from compas.geometry import Point
from compas.geometry import Vector


class VectorArtist(BlenderArtist, PrimitiveArtist):
    """Artist for drawing vectors in Blender.

    Parameters
    ----------
    primitive : :class:`compas.geometry.Vector`
        A COMPAS vector.
    collection : str or :blender:`bpy.types.Collection`
        The Blender scene collection the object(s) created by this artist belong to.
    **kwargs : dict, optional
        Additional keyword arguments.
        For more info,
        see :class:`compas_blender.artists.BlenderArtist` and :class:`compas.artists.PrimitiveArtist`.

    Examples
    --------
    Use the Blender artist explicitly.

    .. code-block:: python

        from compas.geometry import Vector
        from compas_blender.artists import VectorArtist

        vector = Vector(1, 1, 1)

        artist = VectorArtist(vector)
        artist.draw()

    Or, use the artist through the plugin mechanism.

    .. code-block:: python

        from compas.geometry import Vector
        from compas.artists import Artist

        vector = Vector(1, 1, 1)

        artist = Artist(vector)
        artist.draw()

    """

    def __init__(self,
                 vector: Vector,
                 collection: Optional[Union[str, bpy.types.Collection]] = None,
                 **kwargs: Any):
        super().__init__(primitive=vector, collection=collection or vector.name, **kwargs)

    def draw(self,
             color: Optional[RGBColor] = None,
             point: Optional[Point] = None,
             show_point: Optional[bool] = False) -> List[bpy.types.Object]:
        """Draw the vector.

        Parameters
        ----------
        color : tuple[float, float, float] or tuple[int, int, int], optional
            The RGB color of the vector.
            The default color is :attr:`compas.artists.PrimitiveArtist.color`.
        point : [float, float, float] or :class:`compas.geometry.Point`, optional
            Point of application of the vector.
            Default is ``Point(0, 0, 0)``.
        show_point : bool, optional
            If True, draw the point of application of the vector.

        Returns
        -------
        list[:blender:`bpy.types.Object`]

        """
        start = point or (0., 0., 0.)
        end = tuple(map(sum, zip(start, self.primitive)))
        color = color or self. color
        lines = [
            {'start': start, 'end': end, 'color': color, 'name': f"{self.primitive.name}"},
        ]
        objects = compas_blender.draw_lines(lines, self.collection)
        if show_point:
            points = [{
                'pos': start,
                'name': f"{self.primitive.name}.origin",
                'color': (1.0, 1.0, 1.0),
                'radius': 0.01,
            }]
            objects += compas_blender.draw_points(points, self.collection)
        return objects
