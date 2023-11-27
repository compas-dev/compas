from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import scriptcontext as sc  # type: ignore

from compas.artists import GeometryArtist
from compas.colors import Color
from compas_rhino.conversions import point_to_rhino
from .artist import RhinoArtist
from ._helpers import attributes


class FrameArtist(RhinoArtist, GeometryArtist):
    """Artist for drawing frames.

    Parameters
    ----------
    frame: :class:`compas.geometry.Frame`
        A COMPAS frame.
    scale: float, optional
        Scale factor that controls the length of the axes.
    **kwargs : dict, optional
        Additional keyword arguments.

    Attributes
    ----------
    scale : float
        Scale factor that controls the length of the axes.
        Default is ``1.0``.
    color_origin : :class:`compas.colors.Color`
        Default is ``Color.black()``.
    color_xaxis : :class:`compas.colors.Color`
        Default is ``Color.red()``.
    color_yaxis : :class:`compas.colors.Color`
        Default is ``Color.green()``.
    color_zaxis : :class:`compas.colors.Color`
        Default is ``Color.blue()``.

    """

    def __init__(self, frame, scale=1.0, **kwargs):
        super(FrameArtist, self).__init__(geometry=frame, **kwargs)
        self.scale = scale or 1.0
        self.color_origin = Color.black()
        self.color_xaxis = Color.red()
        self.color_yaxis = Color.green()
        self.color_zaxis = Color.blue()

    def draw(self):
        """Draw the frame.

        Returns
        -------
        list[System.Guid]
            The GUIDs of the created Rhino objects.

        """
        guids = []

        attr = attributes(name=self.geometry.name, color=self.color_origin, layer=self.layer)
        guid = sc.doc.Objects.AddPoint(point_to_rhino(self.geometry.point), attr)
        guids.append(guid)

        attr = attributes(name=self.geometry.name, color=self.color_xaxis, layer=self.layer, arrow="end")
        guid = sc.doc.Objects.AddLine(
            point_to_rhino(self.geometry.point),
            point_to_rhino(self.geometry.point + self.geometry.xaxis.scaled(self.scale)),
            attr,
        )
        guids.append(guid)

        attr = attributes(name=self.geometry.name, color=self.color_yaxis, layer=self.layer, arrow="end")
        guid = sc.doc.Objects.AddLine(
            point_to_rhino(self.geometry.point),
            point_to_rhino(self.geometry.point + self.geometry.yaxis.scaled(self.scale)),
            attr,
        )
        guids.append(guid)

        attr = attributes(name=self.geometry.name, color=self.color_zaxis, layer=self.layer, arrow="end")
        guid = sc.doc.Objects.AddLine(
            point_to_rhino(self.geometry.point),
            point_to_rhino(self.geometry.point + self.geometry.zaxis.scaled(self.scale)),
            attr,
        )
        guids.append(guid)

        self.add_to_group("Frame.{}".format(self.geometry.name), guids)

        return guids
