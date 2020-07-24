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
    A : tuple
        The vertices and faces of mesh A.
    B : tuple
        The vertices and faces of mesh B.

    Returns
    -------
    tuple
        The vertices and the faces of the boolean union.
    """
    pass

@pluggable(category='booleans')
def boolean_difference_mesh_mesh(A, B):
    """Compute the boolean difference of two triangle meshes.

    Parameters
    ----------
    A : tuple
        The vertices and faces of mesh A.
    B : tuple
        The vertices and faces of mesh B.

    Returns
    -------
    tuple
        The vertices and the faces of the boolean difference.
    """
    pass


@pluggable(category='booleans')
def boolean_intersection_mesh_mesh(A, B):
    """Compute the boolean intersection of two triangle meshes.

    Parameters
    ----------
    A : tuple
        The vertices and faces of mesh A.
    B : tuple
        The vertices and faces of mesh B.

    Returns
    -------
    tuple
        The vertices and the faces of the boolean intersection.
    """
    pass
