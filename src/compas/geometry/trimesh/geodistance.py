from typing import Literal

from .._tessellation_plugin import tessellation_pluggable
from ..tessellation import Tessellation


@tessellation_pluggable(category="trimesh", inputs=("mesh",))
def trimesh_geodistance(mesh: "Tessellation", source: int, method: Literal["exact", "heat"] = "exact") -> list[float]:
    """Compute geodesic distances from one mesh vertex.

    Parameters
    ----------
    mesh
        The triangle tessellation.
    source
        Index of the source vertex.
    method
        Geodesic algorithm provided by the selected plugin.

    Returns
    -------
    list[float]
        Distance from the source to every mesh vertex.

    Notes
    -----
    This operation requires a registered plugin supporting the requested
    method.

    """
    raise NotImplementedError
