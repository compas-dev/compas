from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from numpy import array
from numpy import cross
from numpy import bincount
from numpy import zeros
from numpy import mean
from numpy import tan
from numpy import arccos
from numpy import sum

from scipy.sparse import spdiags
from scipy.sparse.linalg import splu

from compas.numerical import normrow
from compas.numerical import normalizerow

from compas.datastructures.mesh.core import trimesh_cotangent_laplacian_matrix


__all__ = ['mesh_geodesic_distances_numpy']


def mesh_geodesic_distances_numpy(mesh, sources, m=1.0):
    """Compute geodesic from the vertices of a mesh to given source vertices.

    Parameters
    ----------
    mesh : compas.datastructures.Mesh
        A mesh instance.
    sources : list
        A list of vertex identifiers from which the distances should be calculated.
    m : float (1.0)
        ?

    Returns
    -------
    array
        Distance values.

    """
    Lc = trimesh_cotangent_laplacian_matrix(mesh)

    key_index = mesh.key_index()
    vertices = mesh.vertices_attributes('xyz')
    faces = [[key_index[key] for key in mesh.face_vertices(fkey)] for fkey in mesh.faces()]

    V = array(vertices)
    F = array(faces, dtype=int)

    e01 = V[F[:, 1]] - V[F[:, 0]]
    e12 = V[F[:, 2]] - V[F[:, 1]]
    e20 = V[F[:, 0]] - V[F[:, 2]]

    normal = cross(e01, e12)
    A2 = normrow(normal)
    A3 = A2.ravel() / 6

    VA = zeros(V.shape[0])
    for i in (0, 1, 2):
        b = bincount(F[:, i], A3)
        VA[:len(b)] += b
    VA = spdiags(VA, 0, V.shape[0], V.shape[0])

    h = mean([normrow(e01), normrow(e12), normrow(e20)])
    t = m * h ** 2

    u0 = zeros(V.shape[0])
    u0[sources] = 1.0

    # A = VA - t * Lc
    # print(A.sum(axis=1))

    u = splu((VA - t * Lc).tocsc()).solve(u0)

    unit = normal / A2

    unit_e01 = cross(unit, e01)
    unit_e12 = cross(unit, e12)
    unit_e20 = cross(unit, e20)

    grad_u = (
        unit_e01 * u[F[:, 2], None] +
        unit_e12 * u[F[:, 0], None] +
        unit_e20 * u[F[:, 1], None]) / A2

    X = - grad_u / normrow(grad_u)

    div_X = zeros(V.shape[0])

    for i1, i2, i3 in [(0, 1, 2), (1, 2, 0), (2, 0, 1)]:
        v1 = F[:, i1]
        v2 = F[:, i2]
        v3 = F[:, i3]

        e1 = V[v2] - V[v1]
        e2 = V[v3] - V[v1]
        e0 = V[v3] - V[v2]

        a = 1 / tan(arccos(sum(normalizerow(-e2) * normalizerow(-e0), axis=1)))
        b = 1 / tan(arccos(sum(normalizerow(-e1) * normalizerow(+e0), axis=1)))

        div_X += bincount(
            v1,
            0.5 * (a * sum(e1 * X, axis=1) + b * sum(e2 * X, axis=1)),
            minlength=V.shape[0])

    # print(Lc.sum(axis=1))

    phi = splu(Lc.tocsc()).solve(div_X)
    phi -= phi.min()

    return phi


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    import doctest
    doctest.testmod(globs=globals())
