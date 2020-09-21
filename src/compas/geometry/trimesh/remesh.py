from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas.plugins import pluggable


__all__ = [
    'trimesh_remesh',
    'trimesh_remesh_constrained',
    'trimesh_remesh_along_isoline',
]


@pluggable(category='trimesh')
def trimesh_remesh(mesh, target_edge_length, number_of_iterations=10, do_project=True):
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
    raise NotImplementedError


@pluggable(category='trimesh')
def trimesh_remesh_constrained(mesh, target_edge_length, protected_edges, number_of_iterations=10, do_project=True):
    """Constrained remeshing of a triangle mesh.

    Parameters
    ----------
    mesh : tuple of vertices and faces
        The mesh to remesh.
    target_edge_length : float
        The target edge length.
    protected_edges : list
        A list of vertex pairs that identify protected edges of the mesh.
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

    """
    raise NotImplementedError


@pluggable(category='trimesh')
def trimesh_remesh_along_isoline(mesh, scalarfield, scalar):
    """Remesh a mesh along an isoline of a scalarfield over the vertices.

    Parameters
    ----------
    mesh : tuple or :class:`compas.datastructures.Mesh`
        A mesh represented by a list of vertices and a list of faces
        or a COMPAS mesh object.
    scalarfield : list or array of float
        A scalar value per vertex of the mesh.
    scalar : float
        A value within the range of the scalarfield.

    Returns
    -------
    tuple
        Vertices and faces of the remeshed mesh.

    Examples
    --------
    >>>

    """
    raise NotImplementedError
