from numpy import array

from .trimesh_matrices_numpy import trimesh_cotangent_laplacian_matrix


def trimesh_smooth_laplacian_cotangent(trimesh, fixed, kmax=10):
    """Smooth a triangle mesh using a laplacian matrix with cotangent weights.

    Parameters
    ----------
    trimesh : :class:`compas.datastructures.Mesh`
        A triangle mesh.
    fixed : list[int]
        A list of fixed vertices.
    kmax : int, optional
        The maximum number of smoothing rounds.

    Returns
    -------
    None
        The mesh is modified in place.

    """
    for k in range(kmax):
        V = array(trimesh.vertices_attributes("xyz"))
        L = trimesh_cotangent_laplacian_matrix(trimesh)
        d = L.dot(V)
        V = V + d
        for key, attr in trimesh.vertices(True):
            if key in fixed:
                continue
            attr["x"] = V[key][0]
            attr["y"] = V[key][1]
            attr["z"] = V[key][2]
