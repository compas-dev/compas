import igl
import numpy as np

from compas.plugins import plugin


@plugin(category="trimesh", requires=["igl"])
def trimesh_harmonic(M, boundary, values):
    """Compute the harmonic parametrisation of a triangle mesh within a fixed circular boundary.

    Parameters
    ----------
    M : tuple[sequence[[float, float, float] | :class:`~compas.geometry.Point`], sequence[[int, int, int]]]
        A mesh represented by a list of vertices and a list of faces.
    boundary : list[int]
        The vertices on the boundary.
    values : list[[float, float]]
        The parametrisation values of the boundary vertices.

    Returns
    -------
    list[[int, int]]
        The u, v parameters per vertex.

    Examples
    --------
    >>>

    """
    vertices, faces = M
    V = np.array(vertices, dtype=np.float64)
    F = np.array(faces, dtype=np.int32)
    B = np.array(boundary, dtype=np.int32)
    BC = np.array(values, dtype=np.float64)
    _, uv = igl.lscm(V, F, B, BC)  # type: ignore
    return uv.tolist()


@plugin(category="trimesh", requires=["igl"])
def trimesh_lscm(M, boundary):
    """Compute the least squares conformal map of a triangle mesh.

    Parameters
    ----------
    M : tuple[sequence[[float, float, float] | :class:`~compas.geometry.Point`], sequence[[int, int, int]]]
        A mesh represented by a list of vertices and a list of faces.
    boundary : list[int]
        The vertices on the boundary.

    Returns
    -------
    list[[int, int]]
        The u, v parameters per vertex.

    Examples
    --------
    >>>

    """
    vertices, faces = M
    V = np.array(vertices, dtype=np.float64)
    F = np.array(faces, dtype=np.int32)
    B = np.array([boundary[0], int(len(boundary) / 2)], dtype=np.int32)
    BC = np.array([[0, 0], [1, 0]], dtype=np.float64)
    _, uv = igl.lscm(V, F, B, BC)  # type: ignore
    return uv.tolist()
