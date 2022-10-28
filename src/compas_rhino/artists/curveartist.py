from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino
from compas.artists import CurveArtist
from compas.colors import Color
from .artist import RhinoArtist


class CurveArtist(RhinoArtist, CurveArtist):
    """Artist for drawing curves.

    Parameters
    ----------
    curve : :class:`~compas.geometry.Curve`
        A COMPAS curve.
    layer : str, optional
        The layer that should contain the drawing.
    **kwargs : dict, optional
        Additional keyword arguments.
        For more info, see :class:`RhinoArtist` and :class:`~compas.artists.CurveArtist`.

    """

    def __init__(self, curve, layer=None, **kwargs):
        super(CurveArtist, self).__init__(curve=curve, layer=layer, **kwargs)

    def draw(self, color=None):
        """Draw the curve.

        Parameters
        ----------
        color : tuple[int, int, int] | tuple[float, float, float] | :class:`~compas.colors.Color`, optional
            The RGB color of the curve.
            The default color is :attr:`compas.artists.CurveArtist.color`.

        Returns
        -------
        list[System.Guid]
            The GUIDs of the created Rhino objects.

        """
        color = Color.coerce(color) or self.color
        curves = [{"curve": self.curve, "color": color.rgb255, "name": self.curve.name}]
        return compas_rhino.draw_curves(curves, layer=self.layer, clear=False, redraw=False)
