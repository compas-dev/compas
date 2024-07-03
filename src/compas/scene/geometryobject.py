from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import compas.colors  # noqa: F401
import compas.geometry  # noqa: F401

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

    def __init__(
        self,
        pointcolor=None,  # type: compas.colors.Color | None
        linecolor=None,  # type: compas.colors.Color | None
        surfacecolor=None,  # type: compas.colors.Color | None
        pointsize=1.0,  # type: float
        linewidth=1.0,  # type: float
        show_points=False,  # type: bool
        show_lines=True,  # type: bool
        show_surfaces=True,  # type: bool
        **kwargs  # type: dict
    ):  # fmt: skip
        # type: (...) -> None
        super(GeometryObject, self).__init__(**kwargs)  # type: ignore
        self.pointcolor = pointcolor or self.color
        self.linecolor = linecolor or self.color
        self.surfacecolor = surfacecolor or self.color
        self.pointsize = pointsize
        self.linewidth = linewidth
        self.show_points = show_points
        self.show_lines = show_lines
        self.show_surfaces = show_surfaces

    @property
    def geometry(self):
        # type: () -> compas.geometry.Geometry
        return self.item  # type: ignore
