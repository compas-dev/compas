"""
This package provides plugins for various geometry pluggables using Rhino as the backend.
"""

from __future__ import absolute_import

from .curves.nurbs import RhinoNurbsCurve
from .surfaces.nurbs import RhinoNurbsSurface

from .brep.brep import RhinoBrep
from .brep.loop import RhinoBrepLoop
from .brep.vertex import RhinoBrepVertex
from .brep.face import RhinoBrepFace
from .brep.edge import RhinoBrepEdge
from .brep.trim import RhinoBrepTrim

from .booleans import boolean_difference_mesh_mesh
from .booleans import boolean_union_mesh_mesh
from .booleans import boolean_intersection_mesh_mesh

from .trimesh_curvature import trimesh_gaussian_curvature
from .trimesh_curvature import trimesh_mean_curvature
from .trimesh_curvature import trimesh_principal_curvature

from .trimesh_slicing import trimesh_slice


__all__ = [
    "boolean_difference_mesh_mesh",
    "boolean_intersection_mesh_mesh",
    "boolean_union_mesh_mesh",
    "trimesh_gaussian_curvature",
    "trimesh_mean_curvature",
    "trimesh_principal_curvature",
    "trimesh_slice",
    "RhinoNurbsCurve",
    "RhinoNurbsSurface",
    "RhinoBrep",
    "RhinoBrepVertex",
    "RhinoBrepEdge",
    "RhinoBrepFace",
    "RhinoBrepLoop",
    "RhinoBrepTrim",
]
