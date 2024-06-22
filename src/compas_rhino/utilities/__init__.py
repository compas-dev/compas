from __future__ import absolute_import
from warnings import warn

from ..drawing import (
    draw_labels,
    draw_points,
    draw_lines,
    draw_geodesics,
    draw_polylines,
    draw_breps,
    draw_faces,
    draw_cylinders,
    draw_pipes,
    draw_spheres,
    draw_mesh,
    draw_circles,
    draw_curves,
    draw_surfaces,
    draw_brep,
)

__all__ = [
    "draw_labels",
    "draw_points",
    "draw_lines",
    "draw_geodesics",
    "draw_polylines",
    "draw_breps",
    "draw_faces",
    "draw_cylinders",
    "draw_pipes",
    "draw_spheres",
    "draw_mesh",
    "draw_circles",
    "draw_curves",
    "draw_surfaces",
    "draw_brep",
]

warn("compas_rhino.utilities will be removed in version 2.3. Please use compas_rhino.drawing instead.", DeprecationWarning, stacklevel=2)
