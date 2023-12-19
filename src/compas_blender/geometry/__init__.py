"""
This package provides plugins for various geometry pluggables using Blender as the backend.
"""

from .curves.curve import BlenderCurve  # noqa: F401
from .curves.nurbs import BlenderNurbsCurve  # noqa: F401

from .booleans import boolean_difference_mesh_mesh
from .booleans import boolean_intersection_mesh_mesh
from .booleans import boolean_union_mesh_mesh


__all__ = [
    "boolean_difference_mesh_mesh",
    "boolean_intersection_mesh_mesh",
    "boolean_union_mesh_mesh",
]
