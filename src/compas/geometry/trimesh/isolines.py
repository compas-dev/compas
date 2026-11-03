from collections.abc import Sequence

from .._tessellation_plugin import tessellation_pluggable
from ..tessellation import Tessellation


@tessellation_pluggable(category="trimesh", inputs=("mesh",))
def trimesh_isolines(
    mesh: "Tessellation",
    scalarfield: Sequence[float],
    number_of_isolines: int = 50,
) -> tuple[list[list[float]], list[list[int]]]:
    """Compute isolines of a scalar field on a triangle mesh.

    Parameters
    ----------
    mesh
        The triangle tessellation.
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
