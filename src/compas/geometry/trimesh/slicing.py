from collections.abc import Sequence

from compas._typing import MeshType
from compas.geometry._typing import PlaneType
from compas.plugins import pluggable


@pluggable(category="trimesh")
def trimesh_slice(mesh: MeshType, planes: Sequence[PlaneType]) -> list[list[list[float]]]:
    """Slice a triangle mesh with multiple planes.

    Parameters
    ----------
    mesh
        The mesh vertex coordinates and triangular faces.
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


setattr(trimesh_slice, "__pluggable__", True)
