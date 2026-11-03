from collections.abc import Sequence

from compas.geometry._typing import PlaneType

from .._tessellation_plugin import tessellation_pluggable
from ..tessellation import Tessellation


@tessellation_pluggable(category="trimesh", inputs=("mesh",))
def trimesh_slice(mesh: "Tessellation", planes: Sequence[PlaneType]) -> list[list[list[float]]]:
    """Slice a triangle mesh with multiple planes.

    Parameters
    ----------
    mesh
        The triangle tessellation.
    planes
        The slicing planes.

    Returns
    -------
    list[list[list[float]]]
        Slice polylines represented by lists of point coordinates.

    Notes
    -----
    This operation requires a registered plugin.

    """
    raise NotImplementedError
