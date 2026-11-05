from collections.abc import Sequence

from compas._typing import CoordinatesCollectionInput
from compas._typing import TriangleMeshInput
from compas.geometry._typing import PlaneType
from compas.plugins import pluggable


def trimesh_slice(mesh: TriangleMeshInput, planes: Sequence[PlaneType]) -> CoordinatesCollectionInput:
    """Slice a triangle mesh with multiple planes.

    Parameters
    ----------
    mesh
        The triangle mesh as vertices and triangles.
    planes
        The slicing planes.

    Returns
    -------
    CoordinatesCollectionInput
        Slice polyline coordinate buffers.

    Notes
    -----
    This operation requires a registered plugin.

    """
    return _trimesh_slice(mesh, planes)


@pluggable(category="trimesh")
def _trimesh_slice(mesh: TriangleMeshInput, planes: Sequence[PlaneType]) -> CoordinatesCollectionInput:
    raise NotImplementedError
