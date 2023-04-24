import igl
import numpy as np
from compas.plugins import plugin


@plugin(category="trimesh", requires=["igl"])
def trimesh_gaussian_curvature(M):
    """Compute the discrete gaussian curvature of a triangle mesh.

    Parameters
    ----------
    M : tuple[sequence[[float, float, float] | :class:`~compas.geometry.Point`], sequence[[int, int, int]]]
        A mesh represented by a list of vertices and a list of faces.

    Returns
    -------
    list[float]
        The discrete gaussian curvature per vertex.

    Examples
    --------
    >>>

    """
    vertices, faces = M
    V = np.array(vertices, dtype=np.float64)
    F = np.array(faces, dtype=np.int32)
    k = igl.gaussian_curvature(V, F)  # type: ignore
    return k.tolist()


@plugin(category="trimesh", requires=["igl"])
def trimesh_principal_curvature(M, radius=5, use_k_ring=True):
    """Compute the principal curvature directions of a triangle mesh.

    Parameters
    ----------
    M : tuple[sequence[[float, float, float] | :class:`~compas.geometry.Point`], sequence[[int, int, int]]]
        A mesh represented by a list of vertices and a list of faces.
    radius : int, optional
        The size of the neighbourhood to be used.
    use_k_ring

    Returns
    -------
    tuple[list[[float, float, float]], list[[float, float, float]], list[float], list[float]]
        The maximum curvature direction per vertex.
        The minimum curvature direction per vertex.
        The maximum curvature value per vertex.
        The minimum curvature value per vertex.

    Examples
    --------
    >>>

    """
    vertices, faces = M
    V = np.array(vertices, dtype=np.float64)
    F = np.array(faces, dtype=np.int32)
    maxdir, mindir, maxval, minval = igl.principal_curvature(V, F, radius=radius, use_k_ring=use_k_ring)  # type: ignore
    return maxdir.tolist(), mindir.tolist(), maxval.tolist(), minval.tolist()
