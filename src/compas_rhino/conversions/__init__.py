"""
This package provides functions to convert between COMPAS data/objects and Rhino data/objects.
"""

from __future__ import absolute_import

from .exceptions import ConversionError

from .geometry import (
    point_to_rhino,
    vector_to_rhino,
    plane_to_rhino,
    frame_to_rhino,
    frame_to_rhino_plane,
    polygon_to_rhino,
    point_to_compas,
    vector_to_compas,
    plane_to_compas,
    plane_to_compas_frame,
    polygon_to_compas,
)
from .curves import (
    arc_to_rhino,
    circle_to_rhino,
    circle_to_rhino_curve,
    curve_to_rhino,
    ellipse_to_rhino,
    ellipse_to_rhino_curve,
    line_to_rhino,
    line_to_rhino_curve,
    polyline_to_rhino,
    polyline_to_rhino_curve,
    arc_to_compas,
    circle_to_compas,
    curve_to_compas_circle,
    curve_to_compas_ellipse,
    curve_to_compas_line,
    curve_to_compas_polyline,
    ellipse_to_compas,
    line_to_compas,
    polyline_to_compas,
    curve_to_compas,
)
from .surfaces import (
    surface_to_rhino,
    nurbssurface_to_compas,
    data_to_rhino_surface,
    surface_to_compas_data,
    surface_to_compas,
    surface_to_compas_mesh,
    surface_to_compas_quadmesh,
)
from .shapes import (
    box_to_rhino,
    sphere_to_rhino,
    capsule_to_rhino,
    capsule_to_rhino_brep,
    cone_to_rhino,
    cone_to_rhino_brep,
    cylinder_to_rhino,
    cylinder_to_rhino_brep,
    torus_to_rhino,
    torus_to_rhino_brep,
    box_to_compas,
    sphere_to_compas,
    cone_to_compas,
    cylinder_to_compas,
)
from .meshes import (
    mesh_to_rhino,
    vertices_and_faces_to_rhino,
    mesh_to_compas,
    polyhedron_to_rhino,
)
from .breps import (
    brep_to_rhino,
    brep_to_compas_box,
    brep_to_compas_cone,
    brep_to_compas_cylinder,
    brep_to_compas_sphere,
)
from .extrusions import (
    extrusion_to_compas_box,
    extrusion_to_compas_cylinder,
    extrusion_to_compas_torus,
)

from .transformations import (
    transformation_to_rhino,
    transformation_matrix_to_rhino,
)


__all__ = [
    "ConversionError",
    # geometry
    "point_to_rhino",
    "vector_to_rhino",
    "plane_to_rhino",
    "frame_to_rhino",
    "frame_to_rhino_plane",
    "polygon_to_rhino",
    "point_to_compas",
    "vector_to_compas",
    "plane_to_compas",
    "plane_to_compas_frame",
    "polygon_to_compas",
    # curves
    "line_to_rhino",
    "line_to_rhino_curve",
    "polyline_to_rhino",
    "polyline_to_rhino_curve",
    "circle_to_rhino",
    "circle_to_rhino_curve",
    "ellipse_to_rhino",
    "ellipse_to_rhino_curve",
    "arc_to_rhino",
    "curve_to_rhino",
    "line_to_compas",
    "polyline_to_compas",
    "circle_to_compas",
    "ellipse_to_compas",
    "arc_to_compas",
    "curve_to_compas_circle",
    "curve_to_compas_ellipse",
    "curve_to_compas_line",
    "curve_to_compas_polyline",
    "curve_to_compas",
    # surfaces
    "surface_to_rhino",
    "nurbssurface_to_compas",
    "surface_to_compas_data",
    "data_to_rhino_surface",
    "surface_to_compas",
    "surface_to_compas_mesh",
    "surface_to_compas_quadmesh",
    # shapes
    "box_to_rhino",
    "sphere_to_rhino",
    "capsule_to_rhino",
    "capsule_to_rhino_brep",
    "cone_to_rhino",
    "cone_to_rhino_brep",
    "cylinder_to_rhino",
    "cylinder_to_rhino_brep",
    "torus_to_rhino",
    "torus_to_rhino_brep",
    "box_to_compas",
    "sphere_to_compas",
    "cone_to_compas",
    "cylinder_to_compas",
    # meshes
    "mesh_to_rhino",
    "polyhedron_to_rhino",
    "vertices_and_faces_to_rhino",
    "mesh_to_compas",
    # breps
    "brep_to_rhino",
    "brep_to_compas_box",
    "brep_to_compas_cone",
    "brep_to_compas_cylinder",
    "brep_to_compas_sphere",
    # extrusions
    "extrusion_to_compas_box",
    "extrusion_to_compas_cylinder",
    "extrusion_to_compas_torus",
    # transformations
    "transformation_to_rhino",
    "transformation_matrix_to_rhino",
]
