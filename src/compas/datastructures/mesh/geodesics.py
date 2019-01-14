from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas

try:
    from numpy import array
    from numpy import cross
    from numpy import bincount
    from numpy import zeros
    from numpy import mean
    from numpy import tan
    from numpy import arccos
    from numpy import sum
    from numpy import empty
    from numpy import append
    from numpy import ones

    from scipy.sparse import spdiags
    from scipy.sparse import csr_matrix
    from scipy.sparse.linalg import splu
    from scipy.sparse.linalg import spsolve
    from scipy.linalg import solve

except ImportError:
    compas.raise_if_not_ironpython()


from compas.numerical import normrow
from compas.numerical import normalizerow
from compas.geometry import scalarfield_contours_numpy

from compas.datastructures.mesh.matrices import trimesh_cotangent_laplacian_matrix


__all__ = ['mesh_geodesic_distances']


# def mesh_geodesic_distance_isolines(mesh, sources, m=1.0):
#     distances = mesh_geodesic_distances(mesh, sources, m=m)
#     levels, isolines = scalarfield_isolines_numpy(xy, distances)


def mesh_geodesic_distances(mesh, sources, m=1.0):
    Lc = trimesh_cotangent_laplacian_matrix(mesh)

    key_index = mesh.key_index()
    vertices = mesh.get_vertices_attributes('xyz')
    faces = [[key_index[key] for key in mesh.face_vertices(fkey)] for fkey in mesh.faces()]

    V = array(vertices)
    F = array(faces, dtype=int)

    # Laplacian matrix with symmetric cotangent weights

    # W = empty(0)
    # I = empty(0, dtype=int)
    # J = empty(0, dtype=int)

    # for i1, i2, i3 in [(0, 1, 2), (1, 2, 0), (2, 0, 1)]:
    #     v1 = F[:, i1]
    #     v2 = F[:, i2]
    #     v3 = F[:, i3]

    #     e1 = V[v2] - V[v1]
    #     e2 = V[v3] - V[v1]

    #     cotan = 0.5 * sum(e1 * e2, axis=1) / normrow(cross(e1, e2)).ravel()

    #     W = append(W, cotan)
    #     I = append(I, v2)
    #     J = append(J, v3)

    #     W = append(W, cotan)
    #     I = append(I, v3)
    #     J = append(J, v2)

    # Lc = csr_matrix((W, (I, J)), shape=(V.shape[0], V.shape[0]))
    # Lc = Lc - spdiags(Lc * ones(V.shape[0]), 0, V.shape[0], V.shape[0])

    # Step I
    # Heat *u* is allowed to diffuse for a brief period of time (t)

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

    A = VA - t * Lc

    print(A.sum(axis=1))

    u = splu((VA - t * Lc).tocsc()).solve(u0)
    # u = spsolve(VA - t * Lc, u0)

    # A = VA - t * Lc
    # b = u0
    # u = spsolve(A.transpose().dot(A), A.transpose().dot(b))

    unit = normal / A2

    unit_e01 = cross(unit, e01)
    unit_e12 = cross(unit, e12)
    unit_e20 = cross(unit, e20)

    grad_u = (
        unit_e01 * u[F[:, 2], None] +
        unit_e12 * u[F[:, 0], None] +
        unit_e20 * u[F[:, 1], None]
    ) / A2

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
            minlength=V.shape[0]
        )

    print(Lc.sum(axis=1))

    phi = splu(Lc.tocsc()).solve(div_X)
    # phi = spsolve(Lc, div_X)

    # A = Lc
    # b = div_X
    # phi = spsolve(A.transpose().dot(A), A.transpose().dot(b))

    phi -= phi.min()

    return phi


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    import compas

    from compas.datastructures import Mesh
    from compas.datastructures import mesh_quads_to_triangles
    from compas.datastructures import mesh_flip_cycles

    from compas.plotters import MeshPlotter
    from compas.utilities import i_to_blue
    from compas.geometry import scale_points


    # mesh = Mesh.from_obj(compas.get('models/head-poses/head-reference.obj'))

    mesh = Mesh.from_obj(compas.get('models/camel-poses/camel-reference.obj'))
    mesh_flip_cycles(mesh)

    vertices = scale_points(mesh.get_vertices_attributes('xyz'), 10.0)

    for key, attr in mesh.vertices(True):
        x, y, z = vertices[key]
        attr['x'] = x
        attr['y'] = y
        attr['z'] = z


    # mesh = Mesh.from_obj(compas.get('faces.obj'))
    # mesh_quads_to_triangles(mesh)

    # mesh = Mesh.from_polyhedron(12)
    # mesh_quads_to_triangles(mesh)

    index_key = mesh.index_key()

    sources = [0]

    d = mesh_geodesic_distances(mesh, sources, m=1.0).tolist()

    dmin = min(d)
    dmax = max(d)
    drange = dmax - dmin

    plotter = MeshPlotter(mesh, figsize=(10, 7))

    facecolor = {key: i_to_blue(1 - (d[i] - dmin) / drange) for i, key in enumerate(mesh.vertices())}
    for i in sources:
        facecolor[index_key[i]] = '#ff0000'

    plotter.draw_vertices(
        facecolor=facecolor,
        radius=0.05
    )
    # plotter.draw_edges()
    plotter.draw_faces()

    plotter.show()
