from typing import Literal

from compas._typing import MeshType
from compas.plugins import pluggable


@pluggable(category="trimesh")
def trimesh_geodistance(mesh: MeshType, source: int, method: Literal["exact", "heat"] = "exact") -> list[float]:
    """Compute geodesic distances from one mesh vertex.

    Parameters
    ----------
    mesh
        The mesh vertex coordinates and triangular faces.
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
