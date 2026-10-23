from collections.abc import Sequence

from compas._typing import MeshType
from compas.plugins import pluggable


@pluggable(category="trimesh")
def trimesh_isolines(
    mesh: MeshType,
    scalarfield: Sequence[float],
    number_of_isolines: int = 50,
) -> tuple[list[list[float]], list[list[int]]]:
    """Compute isolines of a scalar field on a triangle mesh.

    Parameters
    ----------
    mesh
        The mesh vertex coordinates and triangular faces.
    scalarfield
        Scalar value at every mesh vertex.
    number_of_isolines
        Number of isolines.

    Returns
    -------
    tuple[list[list[float]], list[list[int]]]
        The generated point coordinates and the isoline segments as pairs of
        point indices.

    Notes
    -----
    This operation requires a registered plugin.

    """
    raise NotImplementedError
