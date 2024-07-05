from __future__ import absolute_import
from warnings import warn

from compas_ghpython.drawing import (
    draw_frame,
    draw_points,
    draw_lines,
    draw_geodesics,
    draw_polylines,
    draw_faces,
    draw_cylinders,
    draw_pipes,
    draw_spheres,
    draw_mesh,
    draw_graph,
    draw_circles,
    draw_brep,
)

__all__ = [
    "draw_frame",
    "draw_points",
    "draw_lines",
    "draw_geodesics",
    "draw_polylines",
    "draw_faces",
    "draw_cylinders",
    "draw_pipes",
    "draw_spheres",
    "draw_mesh",
    "draw_graph",
    "draw_circles",
    "draw_brep",
]

warn("compas_ghpython.utilities will be removed in version 2.3. Please use compas_ghpython.drawing instead.", DeprecationWarning, stacklevel=2)
