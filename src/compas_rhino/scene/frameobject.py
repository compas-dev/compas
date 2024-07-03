from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import scriptcontext as sc  # type: ignore

from compas.colors import Color
from compas.scene import GeometryObject
from compas_rhino.conversions import point_to_rhino
from compas_rhino.conversions import transformation_to_rhino

from .sceneobject import RhinoSceneObject


class RhinoFrameObject(RhinoSceneObject, GeometryObject):
    """Scene object for drawing frames.

    Parameters
    ----------
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

    def __init__(self, scale=1.0, **kwargs):
        super(RhinoFrameObject, self).__init__(**kwargs)
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

        attr = self.compile_attributes(color=self.color_origin)
        guid = sc.doc.Objects.AddPoint(point_to_rhino(self.geometry.point), attr)
        guids.append(guid)

        attr = self.compile_attributes(color=self.color_xaxis, arrow="end")
        guid = sc.doc.Objects.AddLine(
            point_to_rhino(self.geometry.point),
            point_to_rhino(self.geometry.point + self.geometry.xaxis.scaled(self.scale)),
            attr,
        )
        guids.append(guid)

        attr = self.compile_attributes(color=self.color_yaxis, arrow="end")
        guid = sc.doc.Objects.AddLine(
            point_to_rhino(self.geometry.point),
            point_to_rhino(self.geometry.point + self.geometry.yaxis.scaled(self.scale)),
            attr,
        )
        guids.append(guid)

        attr = self.compile_attributes(color=self.color_zaxis, arrow="end")
        guid = sc.doc.Objects.AddLine(
            point_to_rhino(self.geometry.point),
            point_to_rhino(self.geometry.point + self.geometry.zaxis.scaled(self.scale)),
            attr,
        )
        guids.append(guid)

        self.add_to_group("Frame.{}".format(self.geometry.name), guids)
        transformation = transformation_to_rhino(self.worldtransformation)
        for guid in guids:
            obj = sc.doc.Objects.Find(guid)
            if obj:
                obj.Geometry.Transform(transformation)
                obj.CommitChanges()

        self._guids = guids
        return self.guids
