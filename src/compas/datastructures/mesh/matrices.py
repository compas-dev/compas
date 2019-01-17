from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import compas

from compas.geometry import dot_vectors
from compas.geometry import length_vector
from compas.geometry import cross_vectors

from compas.numerical import normrow
from compas.numerical import adjacency_matrix
from compas.numerical import degree_matrix
from compas.numerical import connectivity_matrix
from compas.numerical import laplacian_matrix
from compas.numerical import face_matrix

try:
    from numpy import asarray
    from numpy import ones
    from numpy import zeros
    from numpy import cross
    from numpy import bincount

    from scipy.sparse import coo_matrix
    from scipy.sparse import spdiags

except ImportError:
    compas.raise_if_not_ironpython()


__all__ = [
    'mesh_adjacency_matrix',
    'mesh_degree_matrix',
    'mesh_connectivity_matrix',
    'mesh_laplacian_matrix',
    'mesh_face_matrix',
    'trimesh_cotangent_laplacian_matrix',
    'trimesh_vertexarea_matrix'
]


def mesh_adjacency_matrix(mesh, rtype='array'):
    """Creates a vertex adjacency matrix from a Mesh datastructure.

    Parameters
    ----------
    mesh : obj
        Mesh datastructure object to get data from.
    rtype : {'array', 'csc', 'csr', 'coo', 'list'}
        Format of the result.

    Returns
    -------
    array-like
        Constructed adjacency matrix.

    """
    key_index = mesh.key_index()
    adjacency = [[key_index[nbr] for nbr in mesh.vertex_neighbors(key)] for key in mesh.vertices()]
    return adjacency_matrix(adjacency, rtype=rtype)


def mesh_connectivity_matrix(mesh, rtype='array'):
    """Creates a connectivity matrix from a Mesh datastructure.

    Parameters
    ----------
    mesh : obj
        Mesh datastructure object to get data from.
    rtype : {'array', 'csc', 'csr', 'coo', 'list'}
        Format of the result.

    Returns
    -------
    array-like
        Constructed connectivity matrix.

    """
    key_index = mesh.key_index()
    edges = [(key_index[u], key_index[v]) for u, v in mesh.edges()]
    return connectivity_matrix(edges, rtype=rtype)


def mesh_degree_matrix(mesh, rtype='array'):
    """Creates a vertex degree matrix from a Mesh datastructure.

    Parameters
    ----------
    mesh : obj
        Mesh datastructure object to get data from.
    rtype : {'array', 'csc', 'csr', 'coo', 'list'}
        Format of the result.

    Returns
    -------
    array-like
        Constructed vertex degree matrix.

    """
    key_index = mesh.key_index()
    adjacency = [[key_index[nbr] for nbr in mesh.vertex_neighbors(key)] for key in mesh.vertices()]
    return degree_matrix(adjacency, rtype=rtype)


def mesh_laplacian_matrix(mesh, rtype='csr'):
    """Construct a Laplacian matrix from a Mesh datastructure.

    Parameters
    ----------
    mesh : obj
        Mesh datastructure object to get data from.
    rtype : {'array', 'csc', 'csr', 'coo', 'list'}
        Format of the result.

    Returns
    -------
    array-like
        Constructed Laplacian matrix.

    """
    data, rows, cols = [], [], []
    key_index = mesh.key_index()
    for key in mesh.vertices():
        r = key_index[key]
        data.append(1)
        rows.append(r)
        cols.append(r)
        nbrs = mesh.vertex_neighbors(key)
        w = len(nbrs)
        d = - 1. / w
        for nbr in nbrs:
            c = key_index[nbr]
            data.append(d)
            rows.append(r)
            cols.append(c)
    L = coo_matrix((data, (rows, cols)))
    return L.tocsr()
    # return _return_matrix(L, rtype)


def mesh_face_matrix(mesh, rtype='csr'):
    r"""Construct the face matrix from a Mesh datastructure.

    Parameters
    ----------
    mesh : obj
        Mesh datastructure object to get data from.
    rtype : {'array', 'csc', 'csr', 'coo', 'list'}
        Format of the result.

    Returns
    -------
    array-like
        Constructed mesh face matrix.

    Notes
    -----
    The face matrix represents the relationship between faces and vertices.
    Each row of the matrix represents a face. Each column represents a vertex.
    The matrix is filled with zeros except where a relationship between a vertex
    and a face exist.

    .. math::

        F_{ij} =
        \cases{
            1 & if vertex j is part of face i \cr
            0 & otherwise
        }

    The face matrix can for example be used to compute the centroids of all
    faces of a mesh.

    Examples
    --------
    .. code-block:: python

        import compas
        from compas.datastructures import Mesh
        from compas.numerical import mesh_face_matrix

        mesh = Mesh.from_obj(compas.get('faces.obj'))

        F   = mesh_face_matrix(mesh, 'csr')
        xyz = array([mesh.vertex_coordinates(key) for key in mesh.vertices()])
        c   = F.dot(xyz)

    """
    key_index = {key: index for index, key in enumerate(mesh.vertices())}
    face_vertices = [[key_index[key] for key in mesh.face_vertices(fkey)] for fkey in mesh.faces()]
    return face_matrix(face_vertices, rtype=rtype)


def trimesh_edge_cotangent(mesh, u, v):
    fkey = mesh.halfedge[u][v]
    cotangent = 0.0
    if fkey is not None:
        w = mesh.face_vertex_ancestor(fkey, u)
        wu = mesh.edge_vector(w, u)
        wv = mesh.edge_vector(w, v)
        l = length_vector(cross_vectors(wu, wv))
        if l:
            cotangent = dot_vectors(wu, wv) / l
    return cotangent


def trimesh_edge_cotangents(mesh, u, v):
    a = trimesh_edge_cotangent(mesh, u, v)
    b = trimesh_edge_cotangent(mesh, v, u)
    return a, b


def trimesh_cotangent_laplacian_matrix(mesh):
    r"""Construct the Laplacian of a triangular mesh with cotangent weights.

    Parameters
    ----------
    mesh : obj
        The triangular Mesh datastructure object.

    Returns
    -------
    array
        The Laplacian matrix with cotangent weights.

    Notes
    -----
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

    """
    # minus sum of the adjacent weights on the diagonal
    # cotangent weights on the neighbors
    key_index = mesh.key_index()
    n = mesh.number_of_vertices()
    data = []
    rows = []
    cols = []
    # compute the weight of each halfedge
    # as the cotangent of the angle at the opposite vertex
    for u, v in mesh.edges():
        a, b = trimesh_edge_cotangents(mesh, u, v)
        w = 0.5 * (a + b)
        i = key_index[u]
        j = key_index[v]
        data.append(w)  # not sure why multiplication with 0.5 is necessary
        rows.append(i)
        cols.append(j)
        data.append(w)  # not sure why multiplication with 0.5 is necessary
        rows.append(j)
        cols.append(i)
    L = coo_matrix((data, (rows, cols)), shape=(n, n))
    L = L.tocsr()
    # subtract from the diagonal the sum of the weights of the neighbors of the
    # vertices corresponding to the diagonal entries.
    L = L - spdiags(L * ones(n), 0, n, n)
    return L.tocsr()


def trimesh_positive_cotangent_laplacian_matrix(mesh):
    raise NotImplementedError


def trimesh_vertexarea_matrix(mesh):
    key_index = mesh.key_index()
    xyz = asarray(mesh.get_vertices_attributes('xyz'), dtype=float)
    tris = asarray([[key_index[key] for key in mesh.face_vertices(fkey)] for fkey in mesh.faces()], dtype=int)
    e1 = xyz[tris[:, 1]] - xyz[tris[:, 0]]
    e2 = xyz[tris[:, 2]] - xyz[tris[:, 0]]
    n = cross(e1, e2)
    a = 0.5 * normrow(n).ravel()
    a3 = a / 3.0
    area = zeros(xyz.shape[0])
    for i in (0, 1, 2):
        b = bincount(tris[:, i], a3)
        area[:len(b)] += b
    return spdiags(area, 0, xyz.shape[0], xyz.shape[0])


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    import compas

    from compas.datastructures import Mesh
    from compas.datastructures import mesh_quads_to_triangles

    from compas.plotters import MeshPlotter

    mesh = Mesh.from_obj(compas.get('faces.obj'))

    mesh_quads_to_triangles(mesh)
    A = trimesh_vertexarea_matrix(mesh)
    area = A.diagonal().tolist()

    # area = [mesh.vertex_area(key) for key in mesh.vertices()]

    plotter = MeshPlotter(mesh)

    plotter.draw_vertices(text={key: "{:.3f}".format(area[index]) for index, key in enumerate(mesh.vertices())})
    plotter.draw_edges()
    plotter.draw_faces()

    plotter.show()
