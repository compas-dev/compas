from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas.plugins import pluggable

__all__ = [
    'boolean_union_mesh_mesh',
    'boolean_difference_mesh_mesh',
    'boolean_intersection_mesh_mesh',
]


@pluggable(category='booleans')
def boolean_union_mesh_mesh(A, B):
    """Compute the boolean union of two triangle meshes.

    Parameters
    ----------
    A : (list, list)
        The vertices and faces of mesh A.
    B : (list, list)
        The vertices and faces of mesh B.

    Returns
    -------
    tuple
        The vertices and the faces of the boolean union.

    Examples
    --------
    >>> from compas.geometry import Box, Sphere
    >>> from compas.geometry import boolean_union_mesh_mesh
    >>> from compas.geometry import trimesh_remesh
    >>> from compas.datastructures import Mesh

    >>> box = Box.from_width_height_depth(2, 2, 2)
    >>> box = Mesh.from_shape(box)
    >>> box.quads_to_triangles()

    >>> sphere = Sphere([1, 1, 1], 1)
    >>> sphere = Mesh.from_shape(sphere, u=30, v=30)
    >>> sphere.quads_to_triangles()

    >>> A = box.to_vertices_and_faces()
    >>> B = sphere.to_vertices_and_faces()
    >>> B = trimesh_remesh(B, 0.3, 10)

    >>> V, F = boolean_union_mesh_mesh(A, B)
    >>> union = Mesh.from_vertices_and_faces(V, F)
    """
    raise NotImplementedError


@pluggable(category='booleans')
def boolean_difference_mesh_mesh(A, B):
    """Compute the boolean difference of two triangle meshes.

    Parameters
    ----------
    A : (list, list)
        The vertices and faces of mesh A.
    B : (list, list)
        The vertices and faces of mesh B.

    Returns
    -------
    tuple
        The vertices and the faces of the boolean difference.
    """
    raise NotImplementedError


@pluggable(category='booleans')
def boolean_intersection_mesh_mesh(A, B):
    """Compute the boolean intersection of two triangle meshes.

    Parameters
    ----------
    A : (list, list)
        The vertices and faces of mesh A.
    B : (list, list)
        The vertices and faces of mesh B.

    Returns
    -------
    tuple
        The vertices and the faces of the boolean intersection.
    """
    raise NotImplementedError
