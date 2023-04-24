import igl
import numpy as np
from compas.plugins import plugin


@plugin(category="trimesh", requires=["igl"])
def trimesh_geodistance(M, source, method="exact"):
    """Compute the geodesic distance from every vertex of the mesh to a source vertex.

    Parameters
    ----------
    M : tuple[sequence[[float, float, float] | :class:`~compas.geometry.Point`], sequence[[int, int, int]]]
        A mesh represented by a list of vertices and a list of faces.
    source : int
        The index of the vertex from where the geodesic distances should be calculated.
    method : Literal['exact', 'heat'], optional
        The method for calculating the distances.

    Returns
    -------
    list[float]
        A list of geodesic distances from the source vertex.

    Raises
    ------
    NotImplementedError
        If `method` is not one of ``{'exact', 'heat'}``.

    Examples
    --------
    >>>

    """
    vertices, faces = M
    V = np.array(vertices, dtype=np.float64)
    F = np.array(faces, dtype=np.int32)
    VS = np.array([source], dtype=np.int32)
    VT = np.array(list(range(len(vertices))), dtype=np.int32)
    if method == "exact":
        d = igl.exact_geodesic(V, F, VS, VT)  # type: ignore
    elif method == "heat":
        d = igl.heat_geodesic(V, F, 1.0, VS)  # type: ignore
    else:
        raise NotImplementedError
    return d.tolist()
