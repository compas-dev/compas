from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas.datastructures.mesh.core import BaseMesh

from compas.datastructures.mesh.core import mesh_collapse_edge
from compas.datastructures.mesh.core import mesh_split_edge

from compas.datastructures.mesh.bbox import mesh_bounding_box
from compas.datastructures.mesh.combinatorics import mesh_is_connected
from compas.datastructures.mesh.combinatorics import mesh_connected_components
from compas.datastructures.mesh.duality import mesh_dual
from compas.datastructures.mesh.orientation import mesh_face_adjacency
from compas.datastructures.mesh.orientation import mesh_flip_cycles
from compas.datastructures.mesh.orientation import mesh_unify_cycles

from compas.datastructures.mesh.transformations import mesh_transform
from compas.datastructures.mesh.transformations import mesh_transformed


__all__ = ['Mesh']


class Mesh(BaseMesh):

    collapse_edge = mesh_collapse_edge
    split_edge = mesh_split_edge

    bounding_box = mesh_bounding_box
    is_connected = mesh_is_connected
    connected_components = mesh_connected_components
    dual = mesh_dual
    face_adjacency = mesh_face_adjacency
    flip_cycles = mesh_flip_cycles
    unify_cycles = mesh_unify_cycles

    transform = mesh_transform
    transformed = mesh_transformed

    def to_trimesh(self):
        pass


# =============================================================================
# Main
# =============================================================================

if __name__ == "__main__":
    pass
