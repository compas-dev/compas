from collections.abc import Sequence

from compas._typing import TriangleMeshInput
from compas.plugins import pluggable


def trimesh_remesh(
    mesh: TriangleMeshInput,
    target_edge_length: float,
    number_of_iterations: int = 10,
    do_project: bool = True,
) -> TriangleMeshInput:
    """Remesh a triangle mesh toward a uniform target edge length.

    Parameters
    ----------
    mesh
        The triangle mesh as vertices and triangles.
    target_edge_length
        Target length of mesh edges.
    number_of_iterations
        Maximum number of remeshing iterations.
    do_project
        If `True`, project created or displaced vertices back onto the input
        surface.

    Returns
    -------
    tuple
        The vertices and triangles of the remeshed geometry.

    Notes
    -----
    This operation requires a registered plugin. Core dispatches structural
    buffers without converting or pre-validating them. Use
    [`trimesh_remesh_constrained`][compas.geometry.trimesh_remesh_constrained]
    when specific edges must be preserved.

    """
    return _trimesh_remesh(mesh, target_edge_length, number_of_iterations, do_project)


@pluggable(category="trimesh")
def _trimesh_remesh(
    mesh: TriangleMeshInput,
    target_edge_length: float,
    number_of_iterations: int = 10,
    do_project: bool = True,
) -> TriangleMeshInput:
    raise NotImplementedError


def trimesh_remesh_constrained(
    mesh: TriangleMeshInput,
    target_edge_length: float,
    protected_edges: Sequence[Sequence[int]],
    number_of_iterations: int = 10,
    do_project: bool = True,
) -> TriangleMeshInput:
    """Remesh a triangle mesh while preserving selected edges.

    Parameters
    ----------
    mesh
        The triangle mesh as vertices and triangles.
    target_edge_length
        Target length of mesh edges.
    protected_edges
        Vertex-index pairs identifying edges that must remain unchanged.
    number_of_iterations
        Maximum number of remeshing iterations.
    do_project
        If `True`, project created or displaced vertices back onto the input
        surface.

    Returns
    -------
    tuple
        The vertices and triangles of the remeshed geometry.

    Notes
    -----
    This operation requires a registered plugin. Core dispatches structural
    buffers without converting or pre-validating them.

    """
    return _trimesh_remesh_constrained(mesh, target_edge_length, protected_edges, number_of_iterations, do_project)


@pluggable(category="trimesh")
def _trimesh_remesh_constrained(
    mesh: TriangleMeshInput,
    target_edge_length: float,
    protected_edges: Sequence[Sequence[int]],
    number_of_iterations: int = 10,
    do_project: bool = True,
) -> TriangleMeshInput:
    raise NotImplementedError


def trimesh_remesh_along_isoline(mesh: TriangleMeshInput, scalarfield: Sequence[float], scalar: float) -> TriangleMeshInput:
    """Remesh a triangle mesh so an isoline follows mesh edges.

    Parameters
    ----------
    mesh
        The triangle mesh as vertices and triangles.
    scalarfield
        Scalar value at every mesh vertex.
    scalar
        Isoline value within the scalar-field range.

    Returns
    -------
    tuple
        The vertices and triangles of the remeshed geometry.

    Notes
    -----
    This operation requires a registered plugin. Core dispatches structural
    buffers without converting or pre-validating them. Backend-internal face
    labels are not part of the public result contract.

    """
    return _trimesh_remesh_along_isoline(mesh, scalarfield, scalar)


@pluggable(category="trimesh")
def _trimesh_remesh_along_isoline(
    mesh: TriangleMeshInput,
    scalarfield: Sequence[float],
    scalar: float,
) -> TriangleMeshInput:
    raise NotImplementedError
