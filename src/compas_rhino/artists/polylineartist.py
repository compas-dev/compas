from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import scriptcontext as sc  # type: ignore

from compas.artists import GeometryArtist
from compas.colors import Color
from compas_rhino.conversions import point_to_rhino
from compas_rhino.conversions import polyline_to_rhino
from .artist import RhinoArtist
from ._helpers import attributes


class PolylineArtist(RhinoArtist, GeometryArtist):
    """Artist for drawing polylines.

    Parameters
    ----------
    polyline : :class:`~compas.geometry.Polyline`
        A COMPAS polyline.
    **kwargs : dict, optional
        Additional keyword arguments.
        For more info, see :class:`RhinoArtist` and :class:`GeometryArtist`.

    """

    def __init__(self, polyline, **kwargs):
        super(PolylineArtist, self).__init__(geometry=polyline, **kwargs)

    def draw(self, color=None, show_points=False):
        """Draw the polyline.

        Parameters
        ----------
        color : tuple[int, int, int] | tuple[float, float, float] | :class:`~compas.colors.Color`, optional
            The RGB color of the polyline.
            Default is :attr:`compas.artists.GeometryArtist.color`.
        show_points : bool, optional
            If True, draw the points of the polyline.

        Returns
        -------
        list[System.Guid]
            The GUIDs of the created Rhino objects.

        """
        color = Color.coerce(color) or self.color
        attr = attributes(name=self.geometry.name, color=color, layer=self.layer)

        guid = sc.doc.Objects.AddPolyline(polyline_to_rhino(self.geometry), attr)
        guids = [guid]

        if show_points:
            for point in self.geometry.points:
                guid = sc.doc.Objects.AddPoint(point_to_rhino(point), attr)
                guids.append(guid)

        return guids
