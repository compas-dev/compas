from typing import Any
from typing import Optional
from typing import Union

import bpy  # type: ignore

from compas.artists import GeometryArtist
from compas.geometry import Curve
from compas.colors import Color
from compas_blender.conversions import nurbscurve_to_blender_curve
from compas_blender.artists import BlenderArtist


class CurveArtist(BlenderArtist, GeometryArtist):
    """Artist for drawing curves in Blender.

    Parameters
    ----------
    curve : :class:`~compas.geometry.Curve`
        A COMPAS curve.
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

        from compas.geometry import NurbsCurve
        from compas_blender.artists import CurveArtist

        curve = NurbsCurve([[0, 0, 0], [1, 0, 0], [1, 1, 0], [1, 1, 1]])

        artist = CurveArtist(curve)
        artist.draw()

    Or, use the artist through the plugin mechanism.

    .. code-block:: python

        from compas.geometry import NurbsCurve
        from compas.artists import Artist

        curve = NurbsCurve([[0, 0, 0], [1, 0, 0], [1, 1, 0], [1, 1, 1]])

        artist = Artist(curve)
        artist.draw()

    """

    def __init__(
        self,
        curve: Curve,
        collection: Optional[Union[str, bpy.types.Collection]] = None,
        **kwargs: Any,
    ):
        super().__init__(
            geometry=curve,
            collection=collection or curve.name,
            **kwargs,
        )

    def draw(self, color: Optional[Color] = None) -> bpy.types.Object:
        """Draw the curve.

        Parameters
        ----------
        color : tuple[int, int, int] | tuple[float, float, float] | :class:`~compas.colors.Color`, optional
            The RGB color of the curve.
            The default color is :attr:`compas.artists.CurveArtist.color`.

        Returns
        -------
        :blender:`bpy.types.Object`

        """
        color = Color.coerce(color) or self.color
        curve = nurbscurve_to_blender_curve(self.geometry)

        obj = bpy.data.objects.new(self.geometry.name, curve)

        self.link_object(obj)
        if color:
            self.assign_object_color(obj, color)

        return obj
