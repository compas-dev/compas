from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino
from compas.artists import CurveArtist
from .artist import RhinoArtist


class CurveArtist(RhinoArtist, CurveArtist):
    """Artist for drawing curves.

    Parameters
    ----------
    curve : :class:`compas.geometry.Curve`
        A COMPAS curve.
    layer : str, optional
        The layer that should contain the drawing.
    **kwargs : dict, optional
        Additional keyword arguments.
        For more info, see :class:`RhinoArtist` and :class:`~compas.artists.CurveArtist`.

    """

    def __init__(self, curve, layer=None, **kwargs):
        super(CurveArtist, self).__init__(curve=curve, layer=layer, **kwargs)

    def draw(self, show_points=False):
        """Draw the curve.

        Parameters
        ----------
        show_points : bool, optional
            If True, draw the points of the curve.

        Returns
        -------
        list[System.Guid]
            The GUIDs of the created Rhino objects.

        """
        # _points = map(list, self.curve.points)
        guids = []
        # if show_points:
        #     points = [{'pos': point, 'color': self.color, 'name': self.primitive.name} for point in _points]
        #     guids += compas_rhino.draw_points(points, layer=self.layer, clear=False, redraw=False)
        curves = [{'curve': self.curve, 'color': self.color.rgb255, 'name': self.curve.name}]
        guids += compas_rhino.draw_curves(curves, layer=self.layer, clear=False, redraw=False)
        return guids
