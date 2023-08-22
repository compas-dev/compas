from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import scriptcontext as sc  # type: ignore

from compas.geometry import Point
from compas.artists import GeometryArtist
from compas.colors import Color
from compas_rhino.conversions import point_to_rhino
from .artist import RhinoArtist
from ._helpers import attributes


class VectorArtist(RhinoArtist, GeometryArtist):
    """Artist for drawing vectors.

    Parameters
    ----------
    vector : :class:`~compas.geometry.Vector`
        A COMPAS vector.
    **kwargs : dict, optional
        Additional keyword arguments.
        For more info, see :class:`RhinoArtist` and :class:`GeometryArtist`.

    """

    def __init__(self, vector, **kwargs):
        super(VectorArtist, self).__init__(geometry=vector, **kwargs)

    def draw(self, color=None, point=None, show_point=False):
        """Draw the vector.

        Parameters
        ----------
        color : tuple[int, int, int] | tuple[float, float, float] | :class:`~compas.colors.Color`, optional
            The RGB color of the vector.
            Default is :attr:`compas.artists.GeometryArtist.color`.
        point : [float, float, float] | :class:`~compas.geometry.Point`, optional
            Point of application of the vector.
            Default is ``Point(0, 0, 0)``.
        show_point : bool, optional
            If True, draw the base point of the vector.

        Returns
        -------
        list[System.Guid]
            The GUIDs of the created Rhino objects.

        """
        color = Color.coerce(color) or self.color
        point = point or [0, 0, 0]
        start = Point(*point)
        end = start + self.geometry

        guids = []

        attr = attributes(name=self.geometry.name, color=color, layer=self.layer, arrow="end")
        guid = sc.doc.Objects.AddLine(point_to_rhino(start), point_to_rhino(end), attr)
        guids.append(guid)

        if show_point:
            attr = attributes(name=self.geometry.name, color=color, layer=self.layer)
            guid = sc.doc.Objects.AddPoint(point_to_rhino(start), attr)
            guids.append(guid)

        return guids
