from typing import Any
from typing import Optional

import bpy  # type: ignore

from compas.geometry import Curve
from compas.colors import Color
from compas_blender import conversions

from compas.artists import GeometryArtist
from .artist import BlenderArtist


class CurveArtist(BlenderArtist, GeometryArtist):
    """Artist for drawing curves in Blender.

    Parameters
    ----------
    curve : :class:`~compas.geometry.Curve`
        A COMPAS curve.
    **kwargs : dict, optional
        Additional keyword arguments.

    """

    def __init__(self, curve: Curve, **kwargs: Any):
        super().__init__(geometry=curve, **kwargs)

    def draw(
        self,
        color: Optional[Color] = None,
        collection: Optional[str] = None,
    ) -> bpy.types.Object:
        """Draw the curve.

        Parameters
        ----------
        color : tuple[int, int, int] | tuple[float, float, float] | :class:`~compas.colors.Color`, optional
            The RGB color of the curve.
        collection : str, optional
            The name of the Blender scene collection containing the created object(s).

        Returns
        -------
        :blender:`bpy.types.Object`

        """
        name = self.geometry.name
        color = Color.coerce(color) or self.color
        curve = conversions.nurbscurve_to_blender_curve(self.geometry)

        obj = self.create_object(curve, name=name)
        self.update_object(obj, color=color, collection=collection)

        return obj
