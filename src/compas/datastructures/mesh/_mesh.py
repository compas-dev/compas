from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas.datastructures.mesh.core import BaseMesh
from compas.datastructures.mesh.core import mesh_collapse_edge
from compas.datastructures.mesh.core import mesh_split_edge
from compas.datastructures.mesh.core import mesh_split_face
from compas.datastructures.mesh.core import mesh_merge_faces

from compas.datastructures.mesh.bbox import mesh_bounding_box
from compas.datastructures.mesh.bbox import mesh_bounding_box_xy
from compas.datastructures.mesh.combinatorics import mesh_is_connected
from compas.datastructures.mesh.combinatorics import mesh_connected_components
from compas.datastructures.mesh.duality import mesh_dual
from compas.datastructures.mesh.orientation import mesh_face_adjacency
from compas.datastructures.mesh.orientation import mesh_flip_cycles
from compas.datastructures.mesh.orientation import mesh_unify_cycles
from compas.datastructures.mesh.slice import mesh_slice_plane
from compas.datastructures.mesh.smoothing import mesh_smooth_centroid
from compas.datastructures.mesh.smoothing import mesh_smooth_area
from compas.datastructures.mesh.subdivision import mesh_subdivide
from compas.datastructures.mesh.transformations import mesh_transform
from compas.datastructures.mesh.transformations import mesh_transformed
from compas.datastructures.mesh.triangulation import mesh_quads_to_triangles


__all__ = ['Mesh']


class Mesh(BaseMesh):
    """Implementation of the base mesh data structure that adds some of the mesh algorithms as methods.

    Examples
    --------
    >>> mesh = Mesh.from_polyhedron(6)

    """

    bounding_box = mesh_bounding_box
    bounding_box_xy = mesh_bounding_box_xy
    collapse_edge = mesh_collapse_edge
    connected_components = mesh_connected_components
    dual = mesh_dual
    face_adjacency = mesh_face_adjacency
    flip_cycles = mesh_flip_cycles
    is_connected = mesh_is_connected
    merge_faces = mesh_merge_faces
    slice_plane = mesh_slice_plane
    smooth_centroid = mesh_smooth_centroid
    smooth_area = mesh_smooth_area
    split_edge = mesh_split_edge
    split_face = mesh_split_face
    subdivide = mesh_subdivide
    transform = mesh_transform
    transformed = mesh_transformed
    unify_cycles = mesh_unify_cycles
    quads_to_triangles = mesh_quads_to_triangles
