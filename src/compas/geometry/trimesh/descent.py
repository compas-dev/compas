from typing import TYPE_CHECKING

from compas._typing import MeshType

if TYPE_CHECKING:
    from numpy.typing import NDArray

from .gradient import trimesh_gradient


def trimesh_descent(mesh: MeshType) -> "NDArray":
    """Compute the descent directions of a triangular mesh as the gradient of the vertex heights.

    Parameters
    ----------
    mesh
        The vertices and faces of the mesh.

    Returns
    -------
    numpy.ndarray
        The descent directions.

    """
    from numpy import asarray

    vertices, _ = mesh
    V = asarray(vertices)
    G = trimesh_gradient(mesh)
    sfield = V[:, 2].reshape((-1, 1))
    vfield = -G.dot(sfield)
    return vfield.reshape((-1, 3), order="F")
