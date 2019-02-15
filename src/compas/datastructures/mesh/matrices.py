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
    'mesh_connectivity_matrix',
    'mesh_degree_matrix',
    'mesh_face_matrix',
    'mesh_laplacian_matrix',
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
        \begin{cases}
            1 & \text{if vertex j is part of face i} \\
            0 & \text{otherwise}
        \end{cases}

    The face matrix can for example be used to compute the centroids of all
    faces of a mesh.

    Examples
    --------
    .. code-block:: python

        import compas
        from compas.datastructures import Mesh
        from compas.datastructures import mesh_face_matrix

        mesh = Mesh.from_obj(compas.get('faces.obj'))

        F   = mesh_face_matrix(mesh)
        xyz = array([mesh.vertex_coordinates(key) for key in mesh.vertices()])
        c   = F.dot(xyz) / normrow(F)

    """
    key_index = {key: index for index, key in enumerate(mesh.vertices())}
    face_vertices = [[key_index[key] for key in mesh.face_vertices(fkey)] for fkey in mesh.faces()]
    return face_matrix(face_vertices, rtype=rtype)


def mesh_laplacian_matrix(mesh, rtype='csr'):
    r"""Construct a Laplacian matrix with uniform weights from a mesh data structure.

    The :math:`n \times n` uniform Laplacian matrix :math:`\mathbf{L}` of a mesh
    with vertices :math:`\mathbf{V}` and edges :math:`\mathbf{E}` is defined as
    follows [Nealen]_

    .. math::

        \mathbf{L}_{ij} =
        \begin{cases}
            -1               & i = j \\
            \frac{1}{deg(i)} & (i, j) \in \mathbf{E} \\
            0                & \text{otherwise}
        \end{cases}

    with :math:`deg(i)` the degree of vertex :math:`i`.

    Therefore, the uniform Laplacian of a vertex :math:`\mathbf{v}_{i}` points to
    the centroid of its neighboring vertices.

    Parameters
    ----------
    mesh : obj
        Mesh datastructure object to get data from.
    rtype : {'array', 'csc', 'csr', 'coo', 'list'}
        Format of the result.

    Returns
    -------
    array-like
        The Laplacian matrix.

    Examples
    --------
    .. plot::
        :include-source:

        from random import choice
        from numpy import array

        import compas

        from compas.datastructures import Mesh
        from compas.datastructures import mesh_laplacian_matrix
        from compas.geometry import add_vectors
        from compas.plotters import MeshPlotter

        mesh = Mesh.from_obj(compas.get('faces.obj'))

        key = choice(list(set(mesh.vertices()) - set(mesh.vertices_on_boundary())))

        mesh.vertex[key]['x'] += 0.3
        mesh.vertex[key]['y'] += 0.3

        V = array(mesh.get_vertices_attributes('xyz'))
        L = mesh_laplacian_matrix(mesh)
        d = L.dot(V)

        plotter = MeshPlotter(mesh, tight=True)

        plotter.draw_vertices()
        plotter.draw_edges()
        plotter.draw_faces()

        arrows = []
        for start, vector in zip(V, d):
            arrows.append({
                'start' : start,
                'end'   : add_vectors(start, vector),
                'color' : '#ff0000'
            })

        plotter.draw_arrows(arrows)
        plotter.show()

    References
    ----------
    .. [Nealen] Nealen A., Igarashi T., Sorkine O. and Alexa M. `Laplacian Mesh Optimization <https://igl.ethz.ch/projects/Laplacian-mesh-processing/Laplacian-mesh-optimization/lmo.pdf>`_.

    """
    data, rows, cols = [], [], []
    key_index = mesh.key_index()

    for key in mesh.vertices():
        i = key_index[key]
        nbrs = mesh.vertex_neighbors(key)
        w = len(nbrs)
        data.append(-1.0)
        rows.append(i)
        cols.append(i)
        d = 1.0 / w
        for nbr in nbrs:
            j = key_index[nbr]
            data.append(d)
            rows.append(i)
            cols.append(j)

    L = coo_matrix((data, (rows, cols)))

    if rtype == 'csr':
        return L.tocsr()
    if rtype == 'csc':
        return L.tocsc()
    if rtype == 'array':
        return L.toarray()
    if rtype == 'list':
        return L.toarray().tolist()
    return L


def trimesh_edge_cotangent(mesh, u, v):
    """Compute the cotangent of the angle opposite a halfedge of the triangle mesh.

    Parameters
    ----------
    mesh : compas.datastructures.Mesh
        The triangle mesh data structure.
    u : int
        The identifier of the first vertex of the halfedge.
    v : int
        The identifier of the second vertex of the halfedge.

    Returns
    -------
    float
        The edge cotangent.

    Examples
    --------
    .. code-block:: python

        pass

    """
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
    """Compute the cotangents of the angles opposite both sides of an edge of the triangle mesh.

    Parameters
    ----------
    mesh : compas.datastructures.Mesh
        The triangle mesh data structure.
    u : int
        The identifier of the first vertex of the edge.
    v : int
        The identifier of the second vertex of the edge.

    Returns
    -------
    tuple
        The two edge cotangents.

    Examples
    --------
    .. code-block:: python

        pass

    """
    a = trimesh_edge_cotangent(mesh, u, v)
    b = trimesh_edge_cotangent(mesh, v, u)
    return a, b


def trimesh_cotangent_laplacian_matrix(mesh, rtype='csr'):
    r"""Construct the Laplacian of a triangular mesh with cotangent weights.

    The :math:`n \times n` cotangent Laplacian matrix :math:`\mathbf{L}` of a mesh
    with vertices :math:`\mathbf{V}` and edges :math:`\mathbf{E}` is defined as
    follows [Nealen]_

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


    Parameters
    ----------
    mesh : obj
        The triangular Mesh datastructure object.

    Returns
    -------
    array
        The Laplacian matrix with cotangent weights.

    Examples
    --------
    .. plot::
        :include-source:

        from random import choice
        from numpy import array

        import compas

        from compas.datastructures import Mesh
        from compas.datastructures import trimesh_cotangent_laplacian_matrix
        from compas.datastructures import mesh_quads_to_triangles
        from compas.geometry import add_vectors
        from compas.plotters import MeshPlotter

        mesh = Mesh.from_obj(compas.get('faces.obj'))
        mesh_quads_to_triangles(mesh)

        key = choice(list(set(mesh.vertices()) - set(mesh.vertices_on_boundary())))

        mesh.vertex[key]['x'] += 0.3
        mesh.vertex[key]['y'] += 0.3

        V = array(mesh.get_vertices_attributes('xyz'))
        L = trimesh_cotangent_laplacian_matrix(mesh)
        d = L.dot(V)

        plotter = MeshPlotter(mesh, tight=True)

        plotter.draw_vertices()
        plotter.draw_edges()
        plotter.draw_faces()

        arrows = []
        for start, vector in zip(V, d):
            arrows.append({
                'start' : start,
                'end'   : add_vectors(start, vector),
                'color' : '#ff0000'
            })

        plotter.draw_arrows(arrows)
        plotter.show()

    Notes
    -----
    The cotangent laplacian of a vertex :math:`\mathbf{v}_{i}` points from the vertex
    to the projection of the vertex into the 1-ring plane.
    The cotangent laplacian vectors of a mesh thus provide an approximation of the
    per-vertex normals.

    References
    ----------
    .. [Nealen] Nealen A., Igarashi T., Sorkine O. and Alexa M. `Laplacian Mesh Optimization <https://igl.ethz.ch/projects/Laplacian-mesh-processing/Laplacian-mesh-optimization/lmo.pdf>`_.

    """
    key_index = mesh.key_index()
    n = mesh.number_of_vertices()
    data = []
    rows = []
    cols = []

    for key in mesh.vertices():
        nbrs = mesh.vertex_neighbors(key)
        i = key_index[key]
        data.append(-1.0)
        rows.append(i)
        cols.append(i)

        W = 0
        for nbr in nbrs:
            a, b = trimesh_edge_cotangents(mesh, key, nbr)
            w = a + b
            W += w

        for nbr in nbrs:
            j = key_index[nbr]
            a, b = trimesh_edge_cotangents(mesh, key, nbr)
            w = a + b
            data.append(w / W)
            rows.append(i)
            cols.append(j)

    L = coo_matrix((data, (rows, cols)), shape=(n, n))

    if rtype == 'csr':
        return L.tocsr()
    if rtype == 'csc':
        return L.tocsc()
    if rtype == 'array':
        return L.toarray()
    if rtype == 'list':
        return L.toarray().tolist()
    return L


def trimesh_positive_cotangent_laplacian_matrix(mesh):
    """"""
    raise NotImplementedError


def trimesh_vertexarea_matrix(mesh):
    """Compute the n x n diagonal matrix of per-vertex voronoi areas.

    Parameters
    ----------
    mesh : compas.datastructures.Mesh
        The triangle mesh data structure.

    Returns
    -------
    sparse matrix
        The diagonal voronoi area matrix.

    Examples
    --------
    .. plot::
        :include-source:

        import compas

        from compas.datastructures import Mesh
        from compas.datastructures import mesh_quads_to_triangles
        from compas.datastructures import trimesh_vertexarea_matrix
        from compas.plotters import MeshPlotter

        mesh = Mesh.from_obj(compas.get('faces.obj'))

        mesh_quads_to_triangles(mesh)
        A = trimesh_vertexarea_matrix(mesh)
        area = A.diagonal().tolist()

        plotter = MeshPlotter(mesh, tight=True)

        plotter.draw_vertices(
            text={key: "{:.1f}".format(area[i]) for i, key in enumerate(mesh.vertices())},
            radius=0.2
        )
        plotter.draw_edges()
        plotter.draw_faces()
        plotter.show()

    """
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

    from random import choice
    from numpy import array

    import compas

    from compas.datastructures import Mesh
    from compas.datastructures import mesh_quads_to_triangles
    from compas.geometry import add_vectors

    from compas.plotters import MeshPlotter

    mesh = Mesh.from_obj(compas.get('faces.obj'))

    key = choice(list(set(mesh.vertices()) - set(mesh.vertices_on_boundary())))

    mesh.vertex[key]['x'] += 0.3
    mesh.vertex[key]['y'] += 0.3

    mesh_quads_to_triangles(mesh)
    L = trimesh_cotangent_laplacian_matrix(mesh)
    # L = mesh_laplacian_matrix(mesh)
    xyz = array(mesh.get_vertices_attributes('xyz'))
    d = L.dot(xyz)

    plotter = MeshPlotter(mesh, tight=True)

    plotter.draw_vertices()
    plotter.draw_edges()
    plotter.draw_faces()

    arrows = []
    for start, vector in zip(xyz, d):
        arrows.append({
            'start' : start,
            'end'   : add_vectors(start, vector),
            'color' : '#ff0000'
        })
    plotter.draw_arrows(arrows)

    plotter.show()
