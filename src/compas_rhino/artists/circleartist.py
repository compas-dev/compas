from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import scriptcontext as sc  # type: ignore

from compas.artists import GeometryArtist
from compas.colors import Color
from compas_rhino.conversions import circle_to_rhino
from compas_rhino.conversions import point_to_rhino
from .artist import RhinoArtist
from ._helpers import attributes


class CircleArtist(RhinoArtist, GeometryArtist):
    """Artist for drawing circles.

    Parameters
    ----------
    circle : :class:`~compas.geometry.Circle`
        A COMPAS circle.
    **kwargs : dict, optional
        Additional keyword arguments.
        For more info, see :class:`RhinoArtist` and :class:`GeometryArtist`.

    """

    def __init__(self, circle, **kwargs):
        super(CircleArtist, self).__init__(geometry=circle, **kwargs)

    def draw(self, color=None, show_point=False, show_normal=False):
        """Draw the circle.

        Parameters
        ----------
        color : tuple[int, int, int] | tuple[float, float, float] | :class:`~compas.colors.Color`, optional
            The RGB color of the circle.
            Default is :attr:`compas.artists.GeometryArtist.color`.
        show_point : bool, optional
            If True, draw the center point of the circle.
        show_normal : bool, optional
            If True, draw the normal vector of the circle.

        Returns
        -------
        list[System.Guid]
            The GUIDs of the created Rhino objects.

        """
        color = Color.coerce(color) or self.color
        point = self.geometry.frame.point
        normal = self.geometry.frame.zaxis

        attr = attributes(name=self.geometry.name, color=color, layer=self.layer)
        guid = sc.doc.Objects.AddCircle(circle_to_rhino(self.geometry), attr)
        guids = [guid]

        if show_point:
            guid = sc.doc.Objects.AddPoint(point_to_rhino(point), attr)
            guids.append(guid)

        if show_normal:
            end = point + normal
            attr = attributes(name=self.geometry.name, color=color, layer=self.layer, arrow="end")
            guid = sc.doc.Objects.AddLine(point_to_rhino(point), point_to_rhino(end), attr)
            guids.append(guid)

        return guids
