from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from .core import BaseMesh
from .core import mesh_collapse_edge
from .core import mesh_split_edge
from .core import mesh_split_face
from .core import mesh_merge_faces

from .bbox import mesh_bounding_box
from .bbox import mesh_bounding_box_xy
from .combinatorics import mesh_is_connected
from .combinatorics import mesh_connected_components
from .duality import mesh_dual
from .orientation import mesh_face_adjacency
from .orientation import mesh_flip_cycles
from .orientation import mesh_unify_cycles
from .slice import mesh_slice_plane
from .smoothing import mesh_smooth_centroid
from .smoothing import mesh_smooth_area
from .subdivision import mesh_subdivide
from .transformations import mesh_transform
from .transformations import mesh_transformed
from .triangulation import mesh_quads_to_triangles


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

    def transform_numpy(self, M):
        from compas.datastructures.mesh.transformations_numpy import mesh_transform_numpy
        mesh_transform_numpy(self, M)


# =============================================================================
# Main
# =============================================================================

if __name__ == "__main__":

    import doctest
    doctest.testmod(globs=globals())
