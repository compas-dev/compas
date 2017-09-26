import numpy as np
from scipy import sparse
from scipy.sparse.linalg import splu

from util import veclen, normalized


def compute_mesh_laplacian(verts, tris):
    """
    computes a sparse matrix representing the discretized laplace-beltrami operator of the mesh
    given by n vertex positions ("verts") and a m triangles ("tris")

    verts: (n, 3) array (float)
    tris: (m, 3) array (int) - indices into the verts array

    computes the conformal weights ("cotangent weights") for the mesh, ie:
    w_ij = - .5 * (cot \alpha + cot \beta)

    See:
        Olga Sorkine, "Laplacian Mesh Processing"
        and for theoretical comparison of different discretizations, see
        Max Wardetzky et al., "Discrete Laplace operators: No free lunch"

    returns matrix L that computes the laplacian coordinates, e.g. L * x = delta
    """
    n = len(verts)
    W_ij = np.empty(0)
    I = np.empty(0, np.int32)
    J = np.empty(0, np.int32)
    for i1, i2, i3 in [(0, 1, 2), (1, 2, 0), (2, 0, 1)]:  # for edge i2 --> i3 facing vertex i1
        vi1 = tris[:, i1]  # vertex index of i1
        vi2 = tris[:, i2]
        vi3 = tris[:, i3]
        # vertex vi1 faces the edge between vi2--vi3
        # compute the angle at v1
        # add cotangent angle at v1 to opposite edge v2--v3
        # the cotangent weights are symmetric
        u = verts[vi2] - verts[vi1]
        v = verts[vi3] - verts[vi1]
        cotan = (u * v).sum(axis=1) / veclen(np.cross(u, v))
        W_ij = np.append(W_ij, 0.5 * cotan)
        I = np.append(I, vi2)
        J = np.append(J, vi3)
        W_ij = np.append(W_ij, 0.5 * cotan)
        I = np.append(I, vi3)
        J = np.append(J, vi2)
    L = sparse.csr_matrix((W_ij, (I, J)), shape=(n, n))
    # compute diagonal entries
    L = L - sparse.spdiags(L * np.ones(n), 0, n, n)
    L = L.tocsr()
    # area matrix
    e1 = verts[tris[:, 1]] - verts[tris[:, 0]]
    e2 = verts[tris[:, 2]] - verts[tris[:, 0]]
    n = np.cross(e1, e2)
    triangle_area = .5 * veclen(n)
    # compute per-vertex area
    vertex_area = np.zeros(len(verts))
    ta3 = triangle_area / 3
    for i in xrange(tris.shape[1]):
        bc = np.bincount(tris[:, i].astype(int), ta3)
        vertex_area[:len(bc)] += bc
    VA = sparse.spdiags(vertex_area, 0, len(verts), len(verts))
    return L, VA


class GeodesicDistanceComputation(object):
    """
    Computation of geodesic distances on triangle meshes using the heat method from the impressive paper

        Geodesics in Heat: A New Approach to Computing Distance Based on Heat Flow
        Keenan Crane, Clarisse Weischedel, Max Wardetzky
        ACM Transactions on Graphics (SIGGRAPH 2013)

    Example usage:
        >>> compute_distance = GeodesicDistanceComputation(vertices, triangles)
        >>> distance_of_each_vertex_to_vertex_0 = compute_distance(0)

    """

    def __init__(self, verts, tris, m=10.0):
        self._verts = verts
        self._tris = tris
        # precompute some stuff needed later on
        e01 = verts[tris[:, 1]] - verts[tris[:, 0]]
        e12 = verts[tris[:, 2]] - verts[tris[:, 1]]
        e20 = verts[tris[:, 0]] - verts[tris[:, 2]]
        self._triangle_area = .5 * veclen(np.cross(e01, e12))
        unit_normal = normalized(np.cross(normalized(e01), normalized(e12)))
        self._unit_normal_cross_e01 = np.cross(unit_normal, e01)
        self._unit_normal_cross_e12 = np.cross(unit_normal, e12)
        self._unit_normal_cross_e20 = np.cross(unit_normal, e20)
        # parameters for heat method
        h = np.mean(map(veclen, [e01, e12, e20]))
        t = m * h ** 2
        # pre-factorize poisson systems
        Lc, A = compute_mesh_laplacian(verts, tris)
        self._factored_AtLc = splu((A - t * Lc).tocsc()).solve
        self._factored_L = splu(Lc.tocsc()).solve

    def __call__(self, idx):
        """
        computes geodesic distances to all vertices in the mesh
        idx can be either an integer (single vertex index) or a list of vertex indices
        or an array of bools of length n (with n the number of vertices in the mesh)
        """
        u0 = np.zeros(len(self._verts))
        u0[idx] = 1.0
        # heat method, step 1
        u = self._factored_AtLc(u0).ravel()
        # heat method step 2
        grad_u = 1 / (2 * self._triangle_area)[:, np.newaxis] * (
              self._unit_normal_cross_e01 * u[self._tris[:, 2]][:, np.newaxis] +
              self._unit_normal_cross_e12 * u[self._tris[:, 0]][:, np.newaxis] +
              self._unit_normal_cross_e20 * u[self._tris[:, 1]][:, np.newaxis]
        )
        X = - grad_u / veclen(grad_u)[:, np.newaxis]
        # heat method step 3
        div_Xs = np.zeros(len(self._verts))
        for i1, i2, i3 in [(0, 1, 2), (1, 2, 0), (2, 0, 1)]:  # for edge i2 --> i3 facing vertex i1
            # 0 1 2
            # 1 2 0
            # 2 0 1
            vi1, vi2, vi3 = self._tris[:, i1], self._tris[:, i2], self._tris[:, i3]
            e1 = self._verts[vi2] - self._verts[vi1]
            e2 = self._verts[vi3] - self._verts[vi1]
            e_opp = self._verts[vi3] - self._verts[vi2]
            cot1 = 1 / np.tan(np.arccos(
                (normalized(-e2) * normalized(-e_opp)).sum(axis=1))
            )
            cot2 = 1 / np.tan(np.arccos(
                (normalized(-e1) * normalized(+e_opp)).sum(axis=1))
            )
            div_Xs += np.bincount(
                vi1.astype(int),
                0.5 * (cot1 * (e1 * X).sum(axis=1) + cot2 * (e2 * X).sum(axis=1)),
                minlength=len(self._verts)
            )
        phi  = self._factored_L(div_Xs).ravel()
        phi -= phi.min()
        return phi


# ==============================================================================
# SCRIPT
# ==============================================================================

if __name__ == '__main__':

    import json
    
    from numpy import meshgrid
    from numpy import linspace
    from numpy import amax
    from numpy import amin

    from scipy.interpolate import griddata

    import matplotlib.pyplot as plt

    import brg

    from brg.datastructures import Mesh
    from brg.datastructures.mesh.drawing import draw_mesh

    from brg.utilities import i2red

    mesh = Mesh.from_obj(brg.get_data('faces_big.obj'))

    # mesh = Mesh.from_json('../../../../brg_projects/venice/data/tessellation.json')

    # for fkey in mesh.faces():
    #     vertices = mesh.face_vertices(fkey, ordered=True)
    #     if len(vertices) > 3:
    #         mesh.insert_vertex(fkey)

    key_index = dict((key, index) for index, key in mesh.vertices_enum())
    index_key = dict(mesh.vertices_enum())

    vertices = [mesh.vertex_coordinates(key) for key in mesh.vertex]

    temp = [[key_index[key] for key in mesh.face_vertices(fkey, True)] for fkey in mesh.face]
    faces = []

    for face in temp:
        if len(face) == 3:
            faces.append(face)
        elif len(face) == 4:
            faces.append((face[0], face[1], face[2]))
            faces.append((face[0], face[2], face[3]))

    vertices = np.array(vertices)
    faces = np.array(faces)

    compute_distance = GeodesicDistanceComputation(vertices, faces, 10.0)

    sources = [0, 2000, 4000]

    dist = compute_distance(sources)

    points = vertices
    x      = points[:, 0]
    y      = points[:, 1]
    values = dist
    X, Y   = meshgrid(
       linspace(amin(x), amax(x), 50),
       linspace(amin(y), amax(y), 50)
    )
    Z  = griddata((x, y), values, (X, Y), method='linear')

    ax = plt.gca()

    ax.set_aspect('equal')

    contours = ax.contour(X, Y, Z, 100)

    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_xmargin(0.05)
    ax.set_ymargin(0.05)
    ax.autoscale()

    plt.tight_layout()
    plt.show()

    # isolines = [0] * len(contours.collections)
    # for i, collection in enumerate(iter(contours.collections)):
    #     paths = collection.get_paths()
    #     isolines[i] = [0] * len(paths)
    #     for j, path in enumerate(iter(paths)):
    #         polygons = path.to_polygons()
    #         isolines[i][j] = [0] * len(polygons)
    #         for k, polygon in enumerate(iter(polygons)):
    #             isolines[i][j][k] = polygon.tolist()

    # with open('../../../../brg_projects/venice/data/contours.json', 'wb+') as fp:
    #     json.dump(isolines, fp)

    # vlabels = {}
    # vcolors = {}

    # maxindex, maxval = max(enumerate(dist), key=lambda x: x[1])

    # for key in mesh.vertex:
    #     index = key_index[key]
    #     d = dist[index]
    #     vlabels[key] = '{0:.1f}'.format(d)
    #     if index in sources:
    #         vcolors[key] = 0.0, 0.0, 0.0
    #     else:
    #         vcolors[key] = [comp / 255.0 for comp in i2red(d / maxval)]

    # draw_mesh(mesh, vlabels=[], flabels=[], vcolors=vcolors, vsize=0.1)
