import igl
import numpy as np
from compas.plugins import plugin


@plugin(category="quadmesh", requires=["igl"])
def quadmesh_planarize(mesh, kmax=500, maxdev=0.005):
    """Planarize a quadmesh.

    Parameters
    ----------
    mesh : tuple[list[[float, float, float]], list[[int, int, int, int]]]
        The vertex positions of the quad mesh, and the faces of the quadmesh defined as lists of vertex indices.
    kmax : int, optional
        The maximum number of iterations.
    maxdev : float, optional
        Maximum deviation from flatness.

    Returns
    -------
    list[[float, float, float]]
        The new vertex positions.

    """
    vertices, faces = mesh
    for face in faces:
        if len(face) == 3:
            face.append(face[0])

    F = np.array(faces, dtype=np.int64)
    V = np.array(vertices, dtype=np.float64)
    V = igl.planarize_quad_mesh(V, F, kmax, maxdev)  # type: ignore

    return V.tolist()
