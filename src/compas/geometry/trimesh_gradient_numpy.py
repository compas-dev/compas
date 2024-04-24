import numpy as np
from scipy.sparse import coo_matrix  # type: ignore

from compas.linalg import normalizerow
from compas.linalg import normrow
from compas.linalg import rot90


def trimesh_gradient_numpy(M, rtype="array"):
    """Construct the gradient operator of a trianglular mesh.

    Parameters
    ----------
    V : array
        Vertex coordinates of the mesh.
    F : array
        Face vertex indices of the mesh.
    rtype : {'array', 'csc', 'csr', 'coo', 'list'}
        Format of the result.

    Returns
    -------
    array-like
        Depending on rtype return type.

    Notes
    -----
    The gradient operator is fully determined by the connectivity of the mesh
    and the coordinate difference vectors associated with the edges

    """
    V, F = M
    v = V.shape[0]
    f = F.shape[0]
    f0 = F[:, 0]  # Index of first vertex of each face
    f1 = F[:, 1]  # Index of second vertex of each face
    f2 = F[:, 2]  # Index of last vertex of each face
    v01 = V[f1, :] - V[f0, :]  # Vector from vertex 0 to 1 for each face
    v12 = V[f2, :] - V[f1, :]  # Vector from vertex 1 to 2 for each face
    v20 = V[f0, :] - V[f2, :]  # Vector from vertex 2 to 0 for each face
    n = np.cross(v12, v20)  # Normal vector to each face
    A2 = normrow(n)  # Length of normal vector is twice the area of the face
    A2 = np.tile(A2, (1, 3))
    u = normalizerow(n)  # Unit normals for each face
    v01_ = np.divide(rot90(v01, u), A2)  # Vector perpendicular to v01, normalized by A2
    v20_ = np.divide(rot90(v20, u), A2)  # Vector perpendicular to v20, normalized by A2
    i = np.hstack(
        (  # Nonzero rows
            0 * f + np.tile(np.arange(f), (1, 4)),
            1 * f + np.tile(np.arange(f), (1, 4)),
            2 * f + np.tile(np.arange(f), (1, 4)),
        )
    ).flatten()
    j = np.tile(np.hstack((f1, f0, f2, f0)), (1, 3)).flatten()  # Nonzero columns
    data = np.hstack(
        (
            np.hstack((v20_[:, 0], -v20_[:, 0], v01_[:, 0], -v01_[:, 0])),
            np.hstack((v20_[:, 1], -v20_[:, 1], v01_[:, 1], -v01_[:, 1])),
            np.hstack((v20_[:, 2], -v20_[:, 2], v01_[:, 2], -v01_[:, 2])),
        )
    ).flatten()

    G = coo_matrix((data, (i, j)), shape=(3 * f, v))

    if rtype == "array":
        return G.toarray()
    elif rtype == "csr":
        return G.tocsr()
    elif rtype == "csc":
        return G.tocsc()
    elif rtype == "coo":
        return G
    else:
        return G
