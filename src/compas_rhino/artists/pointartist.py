from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import scriptcontext as sc  # type: ignore

from compas.artists import GeometryArtist
from compas.colors import Color
from compas_rhino.conversions import point_to_rhino
from .artist import RhinoArtist
from ._helpers import attributes


class PointArtist(RhinoArtist, GeometryArtist):
    """Artist for drawing points.

    Parameters
    ----------
    point : :class:`~compas.geometry.Point`
        A COMPAS point.
    **kwargs : dict, optional
        Additional keyword arguments.
        For more info, see :class:`RhinoArtist` and :class:`GeometryArtist`.

    """

    def __init__(self, point, **kwargs):
        super(PointArtist, self).__init__(geometry=point, **kwargs)

    def draw(self, color=None):
        """Draw the point.

        Parameters
        ----------
        color : tuple[int, int, int] | tuple[float, float, float] | :class:`~compas.colors.Color`, optional
            The RGB color of the point.
            Default is :attr:`compas.artists.GeometryArtist.color`.

        Returns
        -------
        list[System.Guid]
            The GUIDs of the created Rhino objects.

        """
        color = Color.coerce(color) or self.color
        attr = attributes(name=self.geometry.name, color=color, layer=self.layer)
        guid = sc.doc.Objects.AddPoint(point_to_rhino(self.geometry), attr)
        return [guid]
