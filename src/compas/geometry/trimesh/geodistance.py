from typing import Literal

from compas._typing import TriangleMeshInput
from compas.plugins import PluginNotInstalledError
from compas.plugins import pluggable


def trimesh_geodistance(mesh: TriangleMeshInput, source: int, method: Literal["exact", "heat"] = "exact") -> list[float]:
    """Compute geodesic distances from one mesh vertex.

    Parameters
    ----------
    mesh
        The triangle mesh as vertices and triangles.
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
    return _trimesh_geodistance(mesh, source, method)


@pluggable(category="trimesh")
def _trimesh_geodistance(mesh: TriangleMeshInput, source: int, method: Literal["exact", "heat"] = "exact") -> list[float]:
    raise PluginNotInstalledError
