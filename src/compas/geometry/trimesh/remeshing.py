from collections.abc import Sequence

from .._tessellation_plugin import tessellation_pluggable
from ..tessellation import Tessellation


@tessellation_pluggable(category="trimesh", inputs=("mesh",), result=True)
def trimesh_remesh(
    mesh: "Tessellation",
    target_edge_length: float,
    number_of_iterations: int = 10,
    do_project: bool = True,
) -> "Tessellation":
    """Remesh a triangle mesh toward a uniform target edge length.

    Parameters
    ----------
    mesh
        The triangle tessellation.
    target_edge_length
        Target length of mesh edges.
    number_of_iterations
        Maximum number of remeshing iterations.
    do_project
        If `True`, project created or displaced vertices back onto the input
        surface.

    Returns
    -------
    Tessellation
        The remeshed triangle geometry.

    Notes
    -----
    This operation requires a registered plugin. Use
    [`trimesh_remesh_constrained`][compas.geometry.trimesh_remesh_constrained]
    when specific edges must be preserved.

    """
    raise NotImplementedError


@tessellation_pluggable(category="trimesh", inputs=("mesh",), result=True)
def trimesh_remesh_constrained(
    mesh: "Tessellation",
    target_edge_length: float,
    protected_edges: Sequence[Sequence[int]],
    number_of_iterations: int = 10,
    do_project: bool = True,
) -> "Tessellation":
    """Remesh a triangle mesh while preserving selected edges.

    Parameters
    ----------
    mesh
        The triangle tessellation.
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
    Tessellation
        The remeshed triangle geometry.

    Notes
    -----
    This operation requires a registered plugin.

    """
    raise NotImplementedError


@tessellation_pluggable(category="trimesh", inputs=("mesh",), result=True)
def trimesh_remesh_along_isoline(mesh: "Tessellation", scalarfield: Sequence[float], scalar: float) -> "Tessellation":
    """Remesh a triangle mesh so an isoline follows mesh edges.

    Parameters
    ----------
    mesh
        The triangle tessellation.
    scalarfield
        Scalar value at every mesh vertex.
    scalar
        Isoline value within the scalar-field range.

    Returns
    -------
    Tessellation
        The remeshed triangle geometry.

    Notes
    -----
    This operation requires a registered plugin. Backend-internal face labels
    are not part of the initial public result contract.

    """
    raise NotImplementedError
