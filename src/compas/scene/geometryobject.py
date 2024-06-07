from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from .descriptors.color import ColorAttribute
from .sceneobject import SceneObject


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
    surfacecolor : :class:`compas.colors.Color`
        The color of the surfaces.
    pointsize : float
        The size of the points.
    linewidth : float
        The width of the lines or curves.
    show_points : bool
        Flag for showing or hiding the points. Default is ``False``.
    show_lines : bool
        Flag for showing or hiding the lines or curves. Default is ``True``.
    show_surfaces : bool
        Flag for showing or hiding the surfaces. Default is ``True``.

    """

    pointcolor = ColorAttribute()
    linecolor = ColorAttribute()
    surfacecolor = ColorAttribute()

    def __init__(self, geometry, **kwargs):
        super(GeometryObject, self).__init__(item=geometry, **kwargs)
        self.geometry = geometry
        self.pointcolor = kwargs.get("pointcolor", self.color)
        self.linecolor = kwargs.get("linecolor", self.color)
        self.surfacecolor = kwargs.get("surfacecolor", self.color)
        self.pointsize = kwargs.get("pointsize", 1.0)
        self.linewidth = kwargs.get("linewidth", 1.0)
        self.show_points = kwargs.get("show_points", False)
        self.show_lines = kwargs.get("show_lines", True)
        self.show_surfaces = kwargs.get("show_surfaces", True)
        # note: either lines should be renamed to curves
        # or surfaces should be renamed to faces?
