from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas_rhino import conversions

from compas.scene import GeometryObject
from .sceneobject import GHSceneObject


class FrameObject(GHSceneObject, GeometryObject):
    """Scene object for drawing frames.

    Parameters
    ----------
    frame : :class:`compas.geometry.Frame`
        A COMPAS frame.
    scale : float, optional
        The scale of the vectors representing the axes of the frame.
    **kwargs : dict, optional
        Additional keyword arguments.

    Attributes
    ----------
    scale : float
        Scale factor that controls the length of the axes.
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
        super(FrameObject, self).__init__(geometry=frame, **kwargs)
        self.scale = scale

    def draw(self):
        """Draw the frame.

        Returns
        -------
        list[:rhino:`Rhino.Geometry.Point3d`, :rhino:`Rhino.Geometry.Line`]
            List of created Rhino geometries.
        """
        geometries = []

        origin = self.geometry.point
        x = self.geometry.point + self.geometry.xaxis * self.scale
        y = self.geometry.point + self.geometry.yaxis * self.scale
        z = self.geometry.point + self.geometry.zaxis * self.scale

        # geometry.append(conversions.frame_to_rhino(self.geometry))
        geometries.append(conversions.point_to_rhino(self.geometry.point))
        geometries.append(conversions.line_to_rhino([origin, x]))
        geometries.append(conversions.line_to_rhino([origin, y]))
        geometries.append(conversions.line_to_rhino([origin, z]))

        for geometry in geometries:
            geometry.Transform(conversions.transformation_to_rhino(self.worldtransformation))

        self._guids = geometries
        return self.guids
