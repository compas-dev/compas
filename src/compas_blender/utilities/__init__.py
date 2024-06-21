from warnings import warn

from ..drawing import (
    draw_circles,
    draw_cylinders,
    draw_cubes,
    draw_faces,
    draw_lines,
    draw_mesh,
    draw_pipes,
    draw_planes,
    draw_pointcloud,
    draw_points,
    draw_polylines,
    draw_spheres,
    draw_texts,
    draw_curves,
    draw_surfaces,
    RGBColor,
)


__all__ = [
    "draw_circles",
    "draw_cylinders",
    "draw_cubes",
    "draw_faces",
    "draw_lines",
    "draw_mesh",
    "draw_pipes",
    "draw_planes",
    "draw_pointcloud",
    "draw_points",
    "draw_polylines",
    "draw_spheres",
    "draw_texts",
    "draw_curves",
    "draw_surfaces",
    "RGBColor",
]

warn("compas_blender.utilities will be removed in version 2.3. Please use compas_blender.drawing instead.", DeprecationWarning, stacklevel=2)
