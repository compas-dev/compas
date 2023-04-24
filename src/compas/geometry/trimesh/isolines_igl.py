import igl
import numpy as np
from compas.plugins import plugin


@plugin(category="trimesh", requires=["igl"])
def trimesh_isolines(M, S, N=50):
    """Compute isolines on a triangle mesh using a scalarfield of data points
    assigned to its vertices.

    Parameters
    ----------
    M : tuple[sequence[[float, float, float] | :class:`~compas.geometry.Point`], sequence[[int, int, int]]]
        A mesh represented by a list of vertices and a list of faces.
    S : list[float]
        A list of scalars.
    N : int, optional
        The number of isolines.

    Returns
    -------
    list[[float, float, float]]
        The coordinates of the polyline points.
    list[[int, int]]
        The segments of the polylines defined as pairs of points.

    Notes
    -----
    To convert the vertices and edges to sets of isolines, use :func:`groupsort_isolines`

    Examples
    --------
    >>>

    """
    vertices, faces = M
    V = np.array(vertices, dtype=np.float64)
    F = np.array(faces, dtype=np.int32)
    S = np.array(S, dtype=np.float64)
    vertices, edges = igl.isolines(V, F, S, N)  # type: ignore
    return vertices.tolist(), edges.tolist()
