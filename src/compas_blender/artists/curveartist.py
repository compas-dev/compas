from typing import Any
from typing import List
from typing import Optional
from typing import Union

import bpy

import compas_blender
from compas.artists import CurveArtist
from compas.geometry import Curve
from compas.colors import Color
from compas_blender.artists import BlenderArtist


class CurveArtist(BlenderArtist, CurveArtist):
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
        see :class:`~compas_blender.artists.BlenderArtist` and :class:`~compas.artists.PrimitiveArtist`.

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

    def __init__(self, curve: Curve, collection: Optional[Union[str, bpy.types.Collection]] = None, **kwargs: Any):

        super().__init__(curve=curve, collection=collection or curve.name, **kwargs)

    def draw(self, color: Optional[Color] = None) -> List[bpy.types.Object]:
        """Draw the curve.

        Parameters
        ----------
        color : tuple[int, int, int] | tuple[float, float, float] | :class:`~compas.colors.Color`, optional
            The RGB color of the curve.
            The default color is :attr:`compas.artists.CurveArtist.color`.

        Returns
        -------
        list[:blender:`bpy.types.Object`]

        """
        color = Color.coerce(color) or self.color
        curves = [{"curve": self.curve, "color": color, "name": self.curve.name}]
        return compas_blender.draw_curves(curves, collection=self.collection)
