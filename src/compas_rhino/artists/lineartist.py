from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import scriptcontext as sc  # type: ignore

from compas.artists import GeometryArtist
from compas.colors import Color
from compas_rhino.conversions import point_to_rhino
from .artist import RhinoArtist
from ._helpers import attributes


class LineArtist(RhinoArtist, GeometryArtist):
    """Artist for drawing lines.

    Parameters
    ----------
    line : :class:`~compas.geometry.Line`
        A COMPAS line.
    **kwargs : dict, optional
        Additional keyword arguments.
        For more info, see :class:`RhinoArtist` and :class:`GeometryArtist`.

    """

    def __init__(self, line, **kwargs):
        super(LineArtist, self).__init__(geometry=line, **kwargs)

    def draw(self, color=None, show_points=False):
        """Draw the line.

        Parameters
        ----------
        color : tuple[int, int, int] | tuple[float, float, float] | :class:`~compas.colors.Color`, optional
            The RGB color of the line.
            Default is :attr:`compas.artists.GeometryArtist.color`.
        show_points : bool, optional
            If True, draw the start and end point of the line.

        Returns
        -------
        list[System.Guid]
            The GUIDs of the created Rhino objects.

        """
        start = point_to_rhino(self.geometry.start)
        end = point_to_rhino(self.geometry.end)
        color = Color.coerce(color) or self.color
        attr = attributes(name=self.geometry.name, color=color, layer=self.layer)

        guid = sc.doc.Objects.AddLine(start, end, attr)
        guids = [guid]

        if show_points:
            guid = sc.doc.Objects.AddPoint(start, attr)
            guids.append(guid)
            guid = sc.doc.Objects.AddPoint(end, attr)
            guids.append(guid)

        return guids
