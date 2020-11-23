from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas.datastructures.mesh.core import BaseMesh
from compas.datastructures.mesh.core import mesh_collapse_edge
from compas.datastructures.mesh.core import mesh_split_edge
from compas.datastructures.mesh.core import mesh_split_face

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
    slice_plane = mesh_slice_plane
    dual = mesh_dual
    face_adjacency = mesh_face_adjacency
    flip_cycles = mesh_flip_cycles
    is_connected = mesh_is_connected
    smooth_centroid = mesh_smooth_centroid
    smooth_area = mesh_smooth_area
    split_edge = mesh_split_edge
    split_face = mesh_split_face
    transform = mesh_transform
    transformed = mesh_transformed
    unify_cycles = mesh_unify_cycles
    quads_to_triangles = mesh_quads_to_triangles

    def transform_numpy(self, M):
        from compas.datastructures.mesh.transformations_numpy import mesh_transform_numpy
        mesh_transform_numpy(self, M)

    def to_trimesh(self):
        # convert to mesh with only triangle faces
        # provides options that define the rules for triangulation
        # for use with trimesh-specific algorithms
        # provide option to use numpy for storage of vertices and faces
        pass

    def to_quadmesh(self):
        pass


# =============================================================================
# Main
# =============================================================================

if __name__ == "__main__":

    import doctest
    doctest.testmod(globs=globals())
