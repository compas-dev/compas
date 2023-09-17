from typing import Any
from typing import Optional

import bpy  # type: ignore

from compas.geometry import Polyline
from compas.colors import Color

from compas.artists import GeometryArtist
from .artist import BlenderArtist

from compas_blender import conversions


class PolylineArtist(BlenderArtist, GeometryArtist):
    """Artist for drawing polylines in Blender.

    Parameters
    ----------
    polyline : :class:`~compas.geometry.Polyline`
        A COMPAS polyline.
    **kwargs : dict, optional
        Additional keyword arguments.
        For more info,
        see :class:`~compas_blender.artists.BlenderArtist` and :class:`~compas.artists.GeometryArtist`.

    """

    def __init__(self, polyline: Polyline, **kwargs: Any):
        super().__init__(geometry=polyline, **kwargs)

    def draw(self, color: Optional[Color] = None, collection: Optional[str] = None) -> bpy.types.Object:
        """Draw the line.

        Parameters
        ----------
        color : tuple[float, float, float] | tuple[int, int, int] | :class:`~compas.colors.Color`, optional
            The RGB color of the polyline.
        collection : str, optional
            The name of the Blender scene collection containing the created object(s).

        Returns
        -------
        :blender:`bpy.types.Object`

        """
        name = self.geometry.name
        color = Color.coerce(color) or self.color

        curve = conversions.polyline_to_blender_curve(self.geometry, name=name)

        obj = self.create_object(curve, name=name)
        self.update_object(obj, color=color, collection=collection)

        return obj
