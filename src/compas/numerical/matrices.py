from __future__ import print_function

from compas.geometry import dot_vectors
from compas.geometry import length_vector
from compas.geometry import cross_vectors

from numpy import abs
from numpy import array
from numpy import asarray
from numpy import float32
from numpy import tile
from numpy import ones

from scipy.sparse import coo_matrix
from scipy.sparse import csr_matrix
from scipy.sparse import diags
from scipy.sparse import spdiags
from scipy.sparse import vstack as svstack


__author__     = ['Tom Van Mele <vanmelet@ethz.ch>',
                  'Andrew Liew <liew@arch.ethz.ch>']
__copyright__  = 'Copyright 2016, Block Research Group - ETH Zurich'
__license__    = 'MIT License'
__email__      = 'vanmelet@ethz.ch'


__all__ = [
    'adjacency_matrix',
    'degree_matrix',
    'connectivity_matrix',
    'laplacian_matrix',
    'face_matrix',
    'mass_matrix',
    'stiffness_matrix',
    'equilibrium_matrix'
]


def _return_matrix(M, rtype):
    if rtype == 'list':
        return M.toarray().tolist()
    if rtype == 'array':
        return M.toarray()
    if rtype == 'csr':
        return M.tocsr()
    if rtype == 'csc':
        return M.tocsc()
    if rtype == 'coo':
        return M.tocoo()
    return M


# ==============================================================================
# adjacency
# ==============================================================================


def adjacency_matrix(adjacency, rtype='array'):
    a = [(1, i, j) for i in range(len(adjacency)) for j in adjacency[i]]
    data, rows, cols = zip(*a)
    A = coo_matrix((data, (rows, cols))).asfptype()
    return _return_matrix(A, rtype)


def face_matrix(face_vertices, rtype='array'):
    """Creates a face-vertex adjacency matrix.

    Parameters:
        face_vertices (list of list) : List of vertices per face.
        rtype (str) : The return type.

    """
    f = array([(i, j, 1) for i, vertices in enumerate(face_vertices) for j in vertices])
    F = coo_matrix((f[:, 2], (f[:, 0], f[:, 1]))).asfptype()
    return _return_matrix(F, rtype)


# def network_adjacency_matrix(network, rtype='array'):
#     key_index = {key: index for index, key in enumerate(network.vertices())}
#     adjacency = [[key_index[nbr] for nbr in network.vertex_neighbours(key)] for key in network.vertices()]
#     return adjacency_matrix(adjacency, rtype=rtype)


# def mesh_adjacency_matrix(mesh, rtype='csr'):
#     key_index = mesh.key_index()
#     adjacency = [[key_index[nbr] for nbr in mesh.vertex_neighbours(key)] for key in mesh.vertices()]
#     return adjacency_matrix(adjacency, rtype=rtype)


# def network_face_matrix(network, rtype='csr'):
#     r"""Construct the face matrix of a network.

#     Parameters:
#         network (compas.datastructures.network.network.Network) :
#             A ``compas`` network datastructure object.
#         rtype (str) : Optional.
#             The type of matrix to be returned. The default is ``'csr'``.

#     Returns:
#         array-like: The face matrix in the format specified by ``rtype``.

#         Possible values of ``rtype`` are ``'list'``, ``'array'``, ``'csr'``, ``'csc'``, ``'coo'``.


#     The face matrix represents the relationship between faces and vertices.
#     Each row of the matrix represents a face. Each column represents a vertex.
#     The matrix is filled with zeros except where a relationship between a vertex
#     and a face exist.

#     .. math::

#         F_{ij} =
#         \cases{
#             1 & if vertex j is part of face i \cr
#             0 & otherwise
#         }

#     The face matrix can for example be used to compute the centroids of all
#     faces of a network.

#     Example:

#         .. code-block:: python

#             import compas
#             from compas.datastructures.network.network import Network

#             network = Network.from_obj(compas.find_resource('lines.obj'))

#             F   = face_matrix(network, 'csr')
#             xyz = array([network.vertex_coordinates(key) for key in network])
#             c   = F.dot(xyz)

#     """
#     key_index = {key: index for index, key in enumerate(network.vertices())}
#     face_vertices = [[key_index[key] for key in network.face_vertices(fkey)] for fkey in network.faces()]
#     return face_matrix(face_vertices, rtype=rtype)


# ==============================================================================
# degree
# ==============================================================================


def degree_matrix(adjacency, rtype='array'):
    d = [(len(adjacency[i]), i, i) for i in range(len(adjacency))]
    data, rows, cols = zip(*d)
    D = coo_matrix((data, (rows, cols))).asfptype()
    return _return_matrix(D, rtype)


# def network_degree_matrix(network, rtype='array'):
#     key_index = {key: index for index, key in enumerate(network.vertices())}
#     adjacency = [[key_index[nbr] for nbr in network.vertex_neighbours(key)] for key in network.vertices()]
#     return degree_matrix(adjacency, rtype=rtype)


# ==============================================================================
# connectivity
# ==============================================================================


def connectivity_matrix(edges, rtype='array'):
    r"""Creates a connectivity matrix from a list of vertex index pairs.

    The connectivity matrix encodes how edges in a network are connected
    together. Each row represents an edge and has 1 and -1 inserted into the
    columns for the start and end nodes.

    .. math::

        \mathbf{C}_{ij} =
        \cases{
            -1 & if edge i starts at vertex j \cr
            +1 & if edge i ends at vertex j \cr
            0  & otherwise
        }

    Note:
        A connectivity matrix is generally sparse and will perform superior
        in numerical calculations as a sparse matrix.

    Parameters:
        edges (list of list): List of lists [[node_i, node_j], [node_k, node_l]].
        rtype (str): Format of the result, 'array', 'csc', 'csr', 'coo'.

    Returns:
        sparse: If ``rtype`` is ``None``, ``'csc'``, ``'csr'``, ``'coo'``.

        array: If ``rtype`` is ``'array'``.

    Examples:
        >>> connectivity_matrix([[0, 1], [0, 2], [0, 3]], rtype='array')
        [[-1  1  0  0]
         [-1  0  1  0]
         [-1  0  0  1]]

    """
    m    = len(edges)
    data = array([-1] * m + [1] * m)
    rows = array(list(range(m)) + list(range(m)))
    cols = array([edge[0] for edge in edges] + [edge[1] for edge in edges])
    C    = coo_matrix((data, (rows, cols))).asfptype()
    return _return_matrix(C, rtype)


# def network_connectivity_matrix(network, rtype='array'):
#     key_index = {key: index for index, key in enumerate(network.vertices())}
#     edges = [(key_index[u], key_index[v]) for u, v in network.edges()]
#     return connectivity_matrix(edges, rtype=rtype)


# def mesh_connectivity_matrix(mesh, rtype='csr'):
#     key_index = mesh.key_index()
#     edges = [(key_index[u], key_index[v]) for u, v in mesh.wireframe()]
#     return connectivity_matrix(edges, rtype=rtype)


# ==============================================================================
# laplacian
# ==============================================================================


# change this to a procedural approach
# constructing (fundamental) matrices should not involve matrix operations
def laplacian_matrix(edges, normalize=False, rtype='array'):
    r"""Creates a laplacian matrix from a list of edge topologies.

    The laplacian matrix is defined as

    .. math::

        \mathbf{L} = \mathbf{C} ^ \mathrm{T} \mathbf{C}

    Note:
        The current implementation only supports umbrella weights,
        as other weighting schemes are not generally applicable.

    See also:
        :func:`compas.datastructures.network.numerical.matrices.network_laplacian_matrix`
        :func:`compas.datastructures.mesh.numerical.matrices.mesh_laplacian_matrix`
        :func:`compas.datastructures.mesh.numerical.matrices.trimesh_cotangent_laplacian_matrix`
        :func:`compas.datastructures.mesh.numerical.matrices.trimesh_positive_cotangent_laplacian_matrix`

    Parameters:
        edges (list of list): List of lists [[node_i, node_j], [node_k, node_l]].
        rtype (str): Format of the result, 'array', 'csc', 'csr', 'coo'.

    Returns:
        sparse: If ''rtype'' is ``None, 'csc', 'csr', 'coo'``.
        array: If ''rtype'' is ``'array'``.

    Examples:
        >>> laplacian_matrix([[0, 1], [0, 2], [0, 3]], rtype='array')
        [[ 3 -1 -1 -1]
         [-1  1  0  0]
         [-1  0  1  0]
         [-1  0  0  1]]

    """
    C = connectivity_matrix(edges, rtype='csr')
    L = C.transpose().dot(C)
    if normalize:
        L = L / L.diagonal().reshape((-1, 1))
        L = csr_matrix(L)
    return _return_matrix(L, rtype)


# def network_laplacian_matrix(network, rtype='array', normalize=False):
#     r"""Construct the Laplacian matrix of a network.

#     Parameters:
#         network (compas.datastructures.network.network.Network) :
#             The network datastructure.

#         rtype (str) :
#             Optional.
#             The format in which the Laplacian should be returned.
#             Default is `'array'`.

#         normalize (bool):
#             Optional.
#             Normalize the entries such that the value on the diagonal is ``1``.
#             Default is ``False``.

#     Returns:
#         array-like: The Laplacian matrix in the format specified by ``rtype``.

#         Possible values of ``rtype`` are ``'list'``, ``'array'``, ``'csr'``, ``'csc'``, ``'coo'``.


#     Note:
#         ``d = L.dot(xyz)`` is currently a vector that points from the centroid to the vertex.
#         Therefore ``c = xyz - d``.
#         By changing the signs in the laplacian,
#         the dsiplacement vectors could be used in a more natural way ``c = xyz + d``.


#     Example:

#         .. plot::
#             :include-source:

#             from numpy import array

#             import compas
#             from compas.datastructures.network import Network
#             from compas.datastructures.network.numerical import network_laplacian_matrix

#             network = Network.from_obj(compas.get_data('grid_irregular.obj'))

#             xy = array([network.vertex_coordinates(key, 'xy') for key in network])
#             L  = network_laplacian_matrix(network, rtype='csr', normalize=True)
#             d  = L.dot(xy)

#             lines = [{'start': xy[i], 'end': xy[i] - d[i]} for i, k in network.vertices_enum()]

#             network.plot(lines=lines)

#     """
#     key_index = {key: index for index, key in enumerate(network.vertices())}
#     edges = [(key_index[u], key_index[v]) for u, v in network.edges()]
#     return laplacian_matrix(edges, normalize=normalize, rtype=rtype)


# def mesh_laplacian_matrix(mesh, rtype='csr'):
#     data, rows, cols = [], [], []
#     key_index = mesh.key_index()
#     for key in mesh.vertices():
#         r = key_index[key]
#         data.append(1)
#         rows.append(r)
#         cols.append(r)
#         # provide anchor clause?
#         nbrs = mesh.vertex_neighbours(key)
#         w = len(nbrs)
#         d = - 1. / w
#         for nbr in nbrs:
#             c = key_index[nbr]
#             data.append(d)
#             rows.append(r)
#             cols.append(c)
#     L = coo_matrix((data, (rows, cols)))
#     return _return_matrix(L, rtype)


def trimesh_edge_cotangent(mesh, u, v):
    fkey = mesh.halfedge[u][v]
    cotangent = 0.0
    if fkey is not None:
        w = mesh.face[fkey][v]  # self.vertex_descendent(v, fkey)
        wu = mesh.edge_vector(w, u)
        wv = mesh.edge_vector(w, v)
        cotangent = dot_vectors(wu, wv) / length_vector(cross_vectors(wu, wv))
    return cotangent


def trimesh_edge_cotangents(mesh, u, v):
    a = trimesh_edge_cotangent(u, v)
    b = trimesh_edge_cotangent(v, u)
    return a, b


def trimesh_cotangent_laplacian_matrix(mesh):
    """Construct the Laplacian of a triangular mesh with cotangent weights.

    Parameters:
        mesh (compas.datastructures.mesh.tri.TriMesh) :
            The triangular mesh.

    Returns:
        array-like :
            The Laplacian matrix with cotangent weights.
            ...

    Note:
        The matrix is constructed such that the diagonal contains the sum of the
        weights of the adjacent vertices, multiplied by `-1`.
        The entries of the matrix are thus

        .. math::

            \mathbf{L}_{ij} =
                \begin{cases}
                    - \sum_{(i, k) \in \mathbf{E}_{i}} w_{ik} & if i = j \\
                    w_{ij} & if (i, j) \in \mathbf{E} \\
                    0 & otherwise
                \end{cases}

    >>> ...

    """
    # minus sum of the adjacent weights on the diagonal
    # cotangent weights on the neighbours
    key_index = mesh.key_index()
    n = mesh.number_of_vertices()
    data = []
    rows = []
    cols = []
    # compute the weight of each halfedge
    # as the cotangent of the angle at the opposite vertex
    for u, v in mesh.wireframe():
        a, b = mesh.edge_cotangents(u, v)
        i = key_index[u]
        j = key_index[v]
        data.append(0.5 * a)  # not sure why multiplication with 0.5 is necessary
        rows.append(i)
        cols.append(j)
        data.append(0.5 * b)  # not sure why multiplication with 0.5 is necessary
        rows.append(j)
        cols.append(i)
    L = coo_matrix((data, (rows, cols)), shape=(n, n))
    L = L.tocsr()
    # subtract from the diagonal the sum of the weights of the neighbours of the
    # vertices corresponding to the diagonal entries.
    L = L - spdiags(L * ones(n), 0, n, n)
    L = L.tocsr()
    return L


def trimesh_positive_cotangent_laplacian_matrix(mesh):
    raise NotImplementedError


# ==============================================================================
# structural
# ==============================================================================


def mass_matrix(Ct, ks, q=0, c=1, tiled=True):
    r"""Creates a network's nodal mass matrix.

    The mass matrix is defined as the sum of the member axial stiffnesses
    (inline) of the elements connected to each node, plus the force density.
    The force density ensures a non-zero value in form-finding/pre-stress
    modelling where E=0.

    .. math::

        \mathbf{m} =
        |\mathbf{C}^\mathrm{T}|
        (\mathbf{E} \circ \mathbf{A} \oslash \mathbf{l} + \mathbf{f} \oslash \mathbf{l})

    Parameters:
        Ct (sparse): Sparse transpose of the connectivity matrix (n x m).
        ks (array): Vector of member EA / L (m x 1).
        q (array): Vector of member force densities (m x 1).
        c (float): Convergence factor.
        tiled (boolean): Whether to tile horizontally by 3 for x, y, z.

    Returns:
        array : mass matrix, either (m x 1) or (m x 3).

    """
    m = c * (abs(Ct).dot(ks + q))
    if tiled:
        return tile(m, (1, 3))
    return m


def stiffness_matrix():
    raise NotImplementedError


def equilibrium_matrix(C, xyz, free, rtype='array'):
    r"""Construct the equilibrium matrix of a structural system.

    Note:
        The matrix of vertex coordinates is vectorised to speed up the
        calculations.

    Parameters:
        C (array, sparse): Connectivity matrix (m x n).
        xyz (array, list): Array of vertex coordinates (n x 3).
        free (list): The index values of the free vertices.
        rtype (str): Format of the result, 'array', 'csc', 'csr', 'coo'.

    Returns:
        sparse : If ``rtype`` is ``'csc', 'csr', 'coo'``.
        array : If ``rtype`` is ``'array'``.

    Analysis of the equilibrium matrix reveals some of the properties of the
    structural system, its size is (2ni x m) where ni is the number of free or
    internal nodes. It is calculated by

    .. math::

        \mathbf{E}
        =
        \left[
            \begin{array}{c}
                \mathbf{C}^{\mathrm{T}}_{\mathrm{i}}\mathbf{U} \\[0.3em]
                \hline \\[-0.7em]
                \mathbf{C}^{\mathrm{T}}_{\mathrm{i}}\mathbf{V}
            \end{array}
        \right].


    Examples:
        >>> C = connectivity_matrix([[0, 1], [0, 2], [0, 3]])
        >>> xyz = [[0, 0, 1], [0, 1, 0], [-1, -1, 0], [1, -1, 0]]
        >>> equilibrium_matrix(C, xyz, [0], rtype='array')
            [[ 0.  1. -1.]
             [-1.  1.  1.]]

    """
    xyz = asarray(xyz, dtype=float32)
    C   = csr_matrix(C)
    xy  = xyz[:, :2]
    uv  = C.dot(xy)
    U   = diags([uv[:, 0].flatten()], [0])
    V   = diags([uv[:, 1].flatten()], [0])
    Ct  = C.transpose()
    Cti = Ct[free, :]
    E   = svstack((Cti.dot(U), Cti.dot(V)))
    return _return_matrix(E, rtype)


# ==============================================================================
# Debugging
# ==============================================================================

if __name__ == "__main__":

    # import compas
    # from compas.datastructures.network import Network

    # from scipy.sparse.linalg import spsolve

    # class Network(Network):
    #     def __init__(self, **kwargs):
    #         super(Network, self).__init__(**kwargs)
    #         self.dea.update({'q': 1.0})

    # network = Network.from_obj(compas.get_data('lines.obj'))

    # k_i = dict((key, index) for index, key in network.vertices_enum())
    # i_k = dict(network.vertices_enum())
    # xyz = [network.vertex_coordinates(key) for key in network]
    # edges = [(k_i[u], k_i[v]) for u, v in network.edges_iter()]
    # n = len(xyz)
    # m = len(edges)
    # fixed = [k_i[key] for key in network.leaves()]
    # free = list(set(range(n)) - set(fixed))
    # q = [float(1.0) for i in range(m)]

    # ij_q = dict(((k_i[u], k_i[v]), attr['q']) for u, v, attr in network.edges_iter(True))
    # ij_q.update(((k_i[v], k_i[u]), attr['q']) for u, v, attr in network.edges_iter(True))

    # xyz = array(xyz)

    # C = connectivity_matrix(edges, 'csr')
    # Q = diags([q], [0])
    # Ci = C[:, free]
    # Cf = C[:, fixed]

    # Cit = Ci.transpose()

    # CitQCi = Cit.dot(Q).dot(Ci)
    # CitQCf = Cit.dot(Q).dot(Cf)

    # print(CitQCf.dot(xyz[fixed]))

    # CtQC = [[0.0 for j in range(n)] for i in range(n)]

    # for i in range(n):
    #     key = i_k[i]
    #     Q = 0
    #     for nbr in network.neighbours(key):
    #         j = k_i[nbr]
    #         q = ij_q[(i, j)]
    #         Q += q
    #         CtQC[i][j] = - q
    #     CtQC[i][i] = Q

    # CitQCi = [[CtQC[i][j] for j in free] for i in free]
    # CitQCf = [[CtQC[i][j] for j in fixed] for i in free]

    # CtQC = array(CtQC)

    # CitQCi = csr_matrix(array(CitQCi))
    # CitQCf = csr_matrix(array(CitQCf))

    # xyz[free] = spsolve(CitQCi, - CitQCf.dot(xyz[fixed]))

    # for key, attr in network.vertices_iter(True):
    #     index = k_i[key]
    #     attr['x'] = xyz[index, 0]
    #     attr['y'] = xyz[index, 1]

    # vlabel = dict((key, str(index)) for index, key in network.vertices_enum())
    # elabel = dict(((u, v), str(index)) for index, u, v in network.edges_enum())

    # network.plot(vlabel=vlabel, elabel=None)

    import compas

    from compas.datastructures.network import Network

    from numpy import allclose

    network = Network.from_obj(compas.get_data('grid_irregular.obj'))

    # key_index = {key: index for index, key in enumerate(network.vertices())}

    # A = network_adjacency_matrix(network)
    # C = network_connectivity_matrix(network)
    # L = network_laplacian_matrix(network, normalize=True, rtype='csr')
    # D = network_degree_matrix(network)

    # xy = [network.vertex_coordinates(key, 'xy') for key in network.vertices()]
    # xy = array(xy, dtype=float).reshape((-1, 2))

    # centroids1 = [network.vertex_neighbourhood_centroid(key) for key in network.vertices()]
    # centroids1 = array(centroids1, dtype=float)[:, 0:2]

    # d = L.dot(xy)

    # centroids2 = xy - d
    # centroids3 = A.dot(xy) / D.diagonal().reshape((-1, 1))

    # print(allclose(centroids1, centroids2))
    # print(allclose(centroids2, centroids3))
    # print(allclose(centroids1, centroids3))
