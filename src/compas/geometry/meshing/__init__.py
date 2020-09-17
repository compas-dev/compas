from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas.plugins import pluggable

__all__ = [
    'remesh',
]


@pluggable(category='meshing')
def remesh(mesh, target_edge_length, number_of_iterations=10, do_project=True):
    """Remeshing of a triangle mesh.

    Parameters
    ----------
    mesh : tuple of vertices and faces
        The mesh to remesh.
    target_edge_length : float
        The target edge length.
    number_of_iterations : int, optional
        Number of remeshing iterations.
        Default is ``10``.
    do_project : bool, optional
        Reproject vertices onto the input surface when they are created or displaced.
        Default is ``True``.

    Returns
    -------
    list
        The vertices and faces of the new mesh.

    Notes
    -----
    This remeshing function only constrains the edges on the boundary of the mesh.
    To protect specific features or edges, please use :func:`remesh_constrained`.

    """
    pass
