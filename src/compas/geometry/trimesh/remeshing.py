from collections.abc import Sequence

from compas._typing import MeshType
from compas.plugins import pluggable

type MeshResult = tuple[list[list[float]], list[list[int]]]


@pluggable(category="trimesh")
def trimesh_remesh(
    mesh: MeshType,
    target_edge_length: float,
    number_of_iterations: int = 10,
    do_project: bool = True,
) -> MeshResult:
    """Remesh a triangle mesh toward a uniform target edge length.

    Parameters
    ----------
    mesh
        The mesh vertex coordinates and triangular faces.
    target_edge_length
        Target length of mesh edges.
    number_of_iterations
        Maximum number of remeshing iterations.
    do_project
        If `True`, project created or displaced vertices back onto the input
        surface.

    Returns
    -------
    tuple[list[list[float]], list[list[int]]]
        The remeshed vertex coordinates and triangular faces.

    Notes
    -----
    This operation requires a registered plugin. Use
    [`trimesh_remesh_constrained`][compas.geometry.trimesh_remesh_constrained]
    when specific edges must be preserved.

    """
    raise NotImplementedError


@pluggable(category="trimesh")
def trimesh_remesh_constrained(
    mesh: MeshType,
    target_edge_length: float,
    protected_edges: Sequence[Sequence[int]],
    number_of_iterations: int = 10,
    do_project: bool = True,
) -> MeshResult:
    """Remesh a triangle mesh while preserving selected edges.

    Parameters
    ----------
    mesh
        The mesh vertex coordinates and triangular faces.
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
    tuple[list[list[float]], list[list[int]]]
        The remeshed vertex coordinates and triangular faces.

    Notes
    -----
    This operation requires a registered plugin.

    """
    raise NotImplementedError


@pluggable(category="trimesh")
def trimesh_remesh_along_isoline(mesh: MeshType, scalarfield: Sequence[float], scalar: float) -> MeshResult:
    """Remesh a triangle mesh so an isoline follows mesh edges.

    Parameters
    ----------
    mesh
        The mesh vertex coordinates and triangular faces.
    scalarfield
        Scalar value at every mesh vertex.
    scalar
        Isoline value within the scalar-field range.

    Returns
    -------
    tuple[list[list[float]], list[list[int]]]
        The remeshed vertex coordinates and triangular faces.

    Notes
    -----
    This operation requires a registered plugin.

    """
    raise NotImplementedError
