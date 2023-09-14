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

    def draw(self, color=None):
        """Draw the polyline.

        Parameters
        ----------
        color : rgb1 | rgb255 | :class:`~compas.colors.Color`, optional
            The RGB color of the polyline.

        Returns
        -------
        System.Guid
            The GUID of the created Rhino object.

        """
        color = Color.coerce(color) or self.color
        attr = attributes(name=self.geometry.name, color=color, layer=self.layer)

        return sc.doc.Objects.AddPolyline(polyline_to_rhino(self.geometry), attr)

    def draw_points(self, color=None):
        """Draw the polyline points.

        Parameters
        ----------
        color : rgb1 | rgb255 | :class:`~compas.colors.Color`, optional
            The RGB color of the polyline points.

        Returns
        -------
        list[System.Guid]
            The GUIDs of the created Rhino objects.

        """
        color = Color.coerce(color) or self.color
        attr = attributes(name=self.geometry.name, color=color, layer=self.layer)

        guids = []

        for point in self.geometry.points:
            guid = sc.doc.Objects.AddPoint(point_to_rhino(point), attr)
            guids.append(guid)

        return guids
