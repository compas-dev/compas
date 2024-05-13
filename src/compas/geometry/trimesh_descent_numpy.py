from numpy import asarray

from .trimesh_gradient_numpy import trimesh_gradient_numpy


def trimesh_descent_numpy(M):
    """Compute the descent directions of a triangular mesh as the gradient of the vertex heights.

    Parameters
    ----------
    M : tuple[vertices, faces]
        The vertices and faces of the mesh.

    Returns
    -------
    list[list[float]]]
        The descent directions.

    """
    vertices, faces = M
    V = asarray(vertices)
    F = asarray(faces)
    G = trimesh_gradient_numpy((V, F))
    sfield = V[:, 2].reshape((-1, 1))
    vfield = -G.dot(sfield)
    return vfield.reshape((-1, 3), order="F")
