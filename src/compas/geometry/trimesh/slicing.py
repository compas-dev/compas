from collections.abc import Sequence

from compas.geometry._typing import PlaneType
from compas.plugins import pluggable
from compas.typing import PointGroupsLike
from compas.typing import VerticesFaces


def trimesh_slice(mesh: VerticesFaces, planes: Sequence[PlaneType]) -> PointGroupsLike:
    """Slice a triangle mesh with multiple planes.

    Parameters
    ----------
    mesh
        The triangle mesh as vertices and triangles.
    planes
        The slicing planes.

    Returns
    -------
    PointGroupsLike
        Slice polyline coordinate buffers.

    Notes
    -----
    This operation requires a registered plugin.

    """
    return _trimesh_slice(mesh, planes)


@pluggable(category="trimesh")
def _trimesh_slice(mesh: VerticesFaces, planes: Sequence[PlaneType]) -> PointGroupsLike:
    raise NotImplementedError
