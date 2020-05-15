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
from compas.datastructures.mesh.cut import mesh_cut_by_plane
from compas.datastructures.mesh.duality import mesh_dual
from compas.datastructures.mesh.orientation import mesh_face_adjacency
from compas.datastructures.mesh.orientation import mesh_flip_cycles
from compas.datastructures.mesh.orientation import mesh_unify_cycles
from compas.datastructures.mesh.smoothing import mesh_smooth_centroid
from compas.datastructures.mesh.smoothing import mesh_smooth_area
from compas.datastructures.mesh.transformations import mesh_transform
from compas.datastructures.mesh.transformations import mesh_transformed


__all__ = ['Mesh']


class Mesh(BaseMesh):
    """Implementation of the base mesh data structure that adds some of the mesh algorithms as methods.

    Examples
    --------
    >>> mesh = Mesh.from_polyhedron(6)
    """

    __module__ = "compas.datastructures"

    bounding_box = mesh_bounding_box
    bounding_box_xy = mesh_bounding_box_xy
    collapse_edge = mesh_collapse_edge
    connected_components = mesh_connected_components
    cut = mesh_cut_by_plane
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

    import compas

    mesh = Mesh.from_obj(compas.get('faces.obj'))

    mesh.update_default_vertex_attributes({'v': 3})
    mesh.update_default_face_attributes({'f': 1})
    mesh.update_default_edge_attributes({'is_edge': True})

    # key = mesh.get_any_vertex()
    # fkey = mesh.get_any_face()
    # ekey = mesh.get_any_edge()

    # mesh.vertex_attribute(key, 'v', 0)
    # mesh.face_attribute(fkey, 'f', 5)
    # mesh.edge_attribute(ekey, 'is_edge', False)

    # print(list(mesh.vertices_where({'v': 0})))
    # print(list(mesh.faces_where({'f': 5})))
    # print(list(mesh.edges_where({'is_edge': False})))

    # # for key, attr in mesh.vertices(True):
    # #     print(key, attr)

    # # for key, attr in mesh.faces(True):
    # #     print(key, attr)

    print()
    print()
    # # for key, attr in mesh.edges(True):
    # #     print(key, attr)

    for key in mesh.edges_on_boundary():
        mesh.edge_attribute(key, 'is_edge', False)

    # print()
    # for key, attr in mesh.edges(True):
    #     print(key, attr)

    # print()
    for key in mesh.edges_where({'is_edge': False}):
        print(key)

    # # print()
    # # for key in mesh.edges_on_boundary():
    # #     print(key, mesh.edge_attribute(key, 'is_edge'))

    # # xyz = mesh.vertices_attributes('xyz')
    # # print(xyz)

    # # attr = mesh.vertex_attributes(0)
    # # print(attr)

    # # attr = mesh.face_attributes(0)
    # # attr.custom_only = True
    # # print(attr)
    # # print(attr.keys())
    # # print(list(attr.keys()))

    # # attr = mesh.edge_attributes((0, 1))
    # # print(attr)

    # # print(mesh)
