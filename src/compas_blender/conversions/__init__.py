"""
This package provides functions to convert between COMPAS data/objects and Blender data/objects.
"""

from .colors import color_to_blender_material

from .geometry import pointcloud_to_blender
from .geometry import polygon_to_blender_mesh
from .geometry import sphere_to_blender_mesh
from .geometry import cylinder_to_blender_mesh

from .transformations import transformation_to_blender
from .transformations import transformation_to_compas

from .curves import line_to_blender_curve
from .curves import polyline_to_blender_curve
from .curves import circle_to_blender_curve
from .curves import nurbscurve_to_blender_curve

from .surfaces import nurbssurface_to_blender_surface

from .meshes import mesh_to_blender
from .meshes import vertices_and_faces_to_blender_mesh
from .meshes import mesh_to_compas
from .meshes import bmesh_to_compas
from .meshes import monkey_to_compas
from .meshes import meshobj_to_compas

__all__ = [
    "color_to_blender_material",
    "pointcloud_to_blender",
    "polygon_to_blender_mesh",
    "sphere_to_blender_mesh",
    "cylinder_to_blender_mesh",
    "line_to_blender_curve",
    "polyline_to_blender_curve",
    "circle_to_blender_curve",
    "nurbscurve_to_blender_curve",
    "nurbssurface_to_blender_surface",
    "mesh_to_blender",
    "vertices_and_faces_to_blender_mesh",
    "mesh_to_compas",
    "bmesh_to_compas",
    "monkey_to_compas",
    "meshobj_to_compas",
    "transformation_to_blender",
    "transformation_to_compas",
]
