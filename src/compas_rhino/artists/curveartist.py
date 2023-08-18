from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino
from compas.artists import GeometryArtist
from compas.colors import Color
from .artist import RhinoArtist


class CurveArtist(RhinoArtist, GeometryArtist):
    """Artist for drawing curves.

    Parameters
    ----------
    curve : :class:`~compas.geometry.Curve`
        A COMPAS curve.
    **kwargs : dict, optional
        Additional keyword arguments.
        For more info, see :class:`RhinoArtist` and :class:`~compas.artists.GeometryArtist`.

    """

    def __init__(self, curve, **kwargs):
        super(CurveArtist, self).__init__(geometry=curve, **kwargs)

    def draw(self, color=None):
        """Draw the curve.

        Parameters
        ----------
        color : tuple[int, int, int] | tuple[float, float, float] | :class:`~compas.colors.Color`, optional
            The RGB color of the curve.
            The default color is :attr:`compas.artists.GeometryArtist.color`.

        Returns
        -------
        list[System.Guid]
            The GUIDs of the created Rhino objects.

        """
        color = Color.coerce(color) or self.color
        curves = [{"curve": self.geometry, "color": color.rgb255, "name": self.geometry.name}]  # type: ignore
        return compas_rhino.draw_curves(curves, layer=self.layer, clear=False, redraw=False)
