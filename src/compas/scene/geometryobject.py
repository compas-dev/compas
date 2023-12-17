from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from .sceneobject import SceneObject
from .descriptors.color import ColorAttribute


class GeometryObject(SceneObject):
    """Base class for scene objects for geometry objects.

    Parameters
    ----------
    geometry : :class:`compas.geometry.Geometry`
        The geometry of the geometry.

    Attributes
    ----------
    geometry : :class:`compas.geometry.Geometry`
        The geometry object associated with the scene object.
    pointcolor : :class:`compas.colors.Color`
        The color of the points.
    linecolor : :class:`compas.colors.Color`
        The color of the lines or curves.
    curvecolor : :class:`compas.colors.Color`
        The color of the lines or curves.
    surfacecolor : :class:`compas.colors.Color`
        The color of the surfaces.
    pointsize : float
        The size of the points.
    linewidth : float
        The width of the lines or curves.

    """

    pointcolor = ColorAttribute()
    curvecolor = linecolor = ColorAttribute()
    surfacecolor = ColorAttribute()

    def __init__(self, geometry, **kwargs):
        super(GeometryObject, self).__init__(item=geometry, **kwargs)
        self.geometry = geometry
        self.pointcolor = kwargs.get("pointcolor", self.color)
        self.linecolor = kwargs.get("linecolor", self.color)
        self.surfacecolor = kwargs.get("surfacecolor", self.color)
        self.pointsize = kwargs.get("pointsize", 1.0)
        self.linewidth = kwargs.get("linewidth", 1.0)
