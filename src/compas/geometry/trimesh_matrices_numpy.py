from numpy import asarray
from numpy import bincount
from numpy import cross
from numpy import zeros
from scipy.sparse import coo_matrix
from scipy.sparse import spdiags

from compas.geometry import cross_vectors
from compas.geometry import dot_vectors
from compas.geometry import length_vector
from compas.linalg import normrow


def trimesh_edge_cotangent(mesh, edge):
    """Compute the cotangent of the angle opposite a halfedge of the triangle mesh.

    Parameters
    ----------
    mesh : :class:`compas.datastructures.Mesh`
        Instance of mesh.
    edge : tuple[int, int]
        The identifier of the halfedge.

    Returns
    -------
    float
        The edge cotangent.

    """
    u, v = edge
    face = mesh.halfedge[u][v]
    cotangent = 0.0
    if face is not None:
        w = mesh.face_vertex_ancestor(face, u)
        wu = mesh.edge_vector((w, u))
        wv = mesh.edge_vector((w, v))
        length = length_vector(cross_vectors(wu, wv))
        if length:
            cotangent = dot_vectors(wu, wv) / length
    return cotangent


def trimesh_edge_cotangents(mesh, edge):
    """Compute the cotangents of the angles opposite both sides of an edge of the triangle mesh.

    Parameters
    ----------
    mesh : :class:`compas.datastructures.Mesh`
        Instance of mesh.
    edge : tuple[int, int]
        The identifier of the edge.

    Returns
    -------
    tuple[float, float]
        The two edge cotangents.

    """
    u, v = edge
    a = trimesh_edge_cotangent(mesh, (u, v))
    b = trimesh_edge_cotangent(mesh, (v, u))
    return a, b


def trimesh_cotangent_laplacian_matrix(mesh, rtype="csr"):
    r"""Construct the Laplacian of a triangular mesh with cotangent weights.

    Parameters
    ----------
    mesh : :class:`compas.datastructures.Mesh`
        Instance of mesh.

    Returns
    -------
    array_like
        The Laplacian matrix with cotangent weights.

    Notes
    -----
    The cotangent laplacian of a vertex :math:`\mathbf{v}_{i}` points from the vertex
    to the projection of the vertex into the 1-ring plane.
    The cotangent laplacian vectors of a mesh thus provide an approximation of the
    per-vertex normals.

    The :math:`n \times n` cotangent Laplacian matrix :math:`\mathbf{L}` of a mesh
    with vertices :math:`\mathbf{V}` and edges :math:`\mathbf{E}` is defined as
    follows [1]_

    .. math::

        \mathbf{L}_{ij} =
            \begin{cases}
                -1      & \text{if i = j} \\
                w_{ij}  & \text{if (i, j) \in \mathbf{E}} \\
                0       & \text{otherwise}
            \end{cases}

    with

    .. math::

         w_{ij} = \frac{\omega_{ij}}{\sum_{(i, k) \in \mathbf{E}_{i}} \omega_{ik}}

    References
    ----------
    .. [1] Nealen A., Igarashi T., Sorkine O. and Alexa M.
        `Laplacian Mesh Optimization <https://igl.ethz.ch/projects/Laplacian-mesh-processing/Laplacian-mesh-optimization/lmo.pdf>`_.

    """
    vertex_index = mesh.vertex_index()
    n = mesh.number_of_vertices()
    data = []
    rows = []
    cols = []

    for vertex in mesh.vertices():
        nbrs = mesh.vertex_neighbors(vertex)
        i = vertex_index[vertex]
        data.append(-1.0)
        rows.append(i)
        cols.append(i)

        W = 0
        for nbr in nbrs:
            a, b = trimesh_edge_cotangents(mesh, (vertex, nbr))
            w = a + b
            W += w

        for nbr in nbrs:
            j = vertex_index[nbr]
            a, b = trimesh_edge_cotangents(mesh, (vertex, nbr))
            w = a + b
            data.append(w / W)
            rows.append(i)
            cols.append(j)

    L = coo_matrix((data, (rows, cols)), shape=(n, n))

    if rtype == "csr":
        return L.tocsr()
    if rtype == "csc":
        return L.tocsc()
    if rtype == "array":
        return L.toarray()
    if rtype == "list":
        return L.toarray().tolist()
    return L


def trimesh_positive_cotangent_laplacian_matrix(mesh):
    raise NotImplementedError


def trimesh_vertexarea_matrix(mesh):
    """Compute the n x n diagonal matrix of per-vertex voronoi areas.

    Parameters
    ----------
    mesh : :class:`compas.datastructures.Mesh`
        The triangle mesh data structure.

    Returns
    -------
    sparse matrix
        The diagonal voronoi area matrix.

    Examples
    --------
    >>> from compas.datastructures import Mesh
    >>> mesh = Mesh.from_polygons([[[0, 0, 0], [1, 0, 0], [0, 1, 0]]])
    >>> A = trimesh_vertexarea_matrix(mesh)
    >>> A.diagonal().tolist()
    [0.1666, 0.1666, 0.1666]

    """
    vertex_index = mesh.vertex_index()
    xyz = asarray(mesh.vertices_attributes("xyz"), dtype=float)
    tris = asarray(
        [[vertex_index[vertex] for vertex in mesh.face_vertices(face)] for face in mesh.faces()],
        dtype=int,
    )
    e1 = xyz[tris[:, 1]] - xyz[tris[:, 0]]
    e2 = xyz[tris[:, 2]] - xyz[tris[:, 0]]
    n = cross(e1, e2)
    a = 0.5 * normrow(n).ravel()
    a3 = a / 3.0
    area = zeros(xyz.shape[0])
    for i in (0, 1, 2):
        b = bincount(tris[:, i], a3)
        area[: len(b)] += b
    return spdiags(area, 0, xyz.shape[0], xyz.shape[0])
