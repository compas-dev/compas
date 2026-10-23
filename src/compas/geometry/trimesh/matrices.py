from typing import TYPE_CHECKING
from typing import Any
from typing import Literal
from typing import overload

from compas._typing import MeshType
from compas.linalg.vectors import cross_vectors
from compas.linalg.vectors import dot_vectors
from compas.linalg.vectors import length_vector
from compas.plugins import pluggable

if TYPE_CHECKING:
    from numpy.typing import NDArray
    from scipy.sparse import coo_array
    from scipy.sparse import coo_matrix
    from scipy.sparse import csc_array
    from scipy.sparse import csc_matrix
    from scipy.sparse import csr_array
    from scipy.sparse import csr_matrix
    from scipy.sparse import dia_matrix

    from compas.datastructures import Mesh
    from compas.datastructures.mesh.types import Edge


@pluggable(category="trimesh")
def trimesh_massmatrix(mesh: MeshType) -> list[float]:
    """Compute the per-vertex mass matrix of a triangle mesh.

    Parameters
    ----------
    mesh
        The mesh vertex coordinates and triangular faces.

    Returns
    -------
    list[float]
        The mass associated with every vertex.

    Notes
    -----
    This operation requires a registered plugin.

    """
    raise NotImplementedError


setattr(trimesh_massmatrix, "__pluggable__", True)


def trimesh_edge_cotangent(mesh: "Mesh", edge: "Edge") -> float:
    """Compute the cotangent of the angle opposite a halfedge of the triangle mesh.

    Parameters
    ----------
    mesh : Mesh
        The triangle mesh.
    edge : tuple[int, int]
        The directed edge identifying the halfedge.

    Returns
    -------
    float
        The cotangent of the opposite angle, or `0.0` for a boundary
        halfedge without an incident face.

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


def trimesh_edge_cotangents(mesh: "Mesh", edge: "Edge") -> tuple[float, float]:
    """Compute the cotangents of the angles opposite both sides of an edge of the triangle mesh.

    Parameters
    ----------
    mesh : Mesh
        The triangle mesh.
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


@overload
def trimesh_cotangent_laplacian_matrix(mesh: "Mesh", rtype: Literal["csr"] = "csr") -> "csr_matrix | csr_array": ...


@overload
def trimesh_cotangent_laplacian_matrix(mesh: "Mesh", rtype: Literal["csc"]) -> "csc_matrix | csc_array": ...


@overload
def trimesh_cotangent_laplacian_matrix(mesh: "Mesh", rtype: Literal["array"]) -> "NDArray[Any]": ...


@overload
def trimesh_cotangent_laplacian_matrix(mesh: "Mesh", rtype: Literal["list"]) -> list[list[float]]: ...


@overload
def trimesh_cotangent_laplacian_matrix(
    mesh: "Mesh", rtype: str
) -> "coo_matrix | coo_array | csc_matrix | csc_array | csr_matrix | csr_array | NDArray[Any] | list[list[float]]": ...


def trimesh_cotangent_laplacian_matrix(
    mesh: "Mesh", rtype: str = "csr"
) -> "coo_matrix | coo_array | csc_matrix | csc_array | csr_matrix | csr_array | NDArray[Any] | list[list[float]]":
    r"""Construct the cotangent Laplacian matrix of a triangle mesh.

    Parameters
    ----------
    mesh : Mesh
        The triangle mesh.
    rtype : {`"csr"`, `"csc"`, `"array"`, `"list"`}, optional
        Requested matrix representation. Any other value returns a SciPy COO
        sparse matrix.

    Returns
    -------
    scipy.sparse.spmatrix | numpy.ndarray | list[list[float]]
        The row-normalized cotangent Laplacian in the requested representation.

    Raises
    ------
    ValueError
        If the cotangent weights at a vertex sum to zero and therefore cannot
        be normalized.

    Notes
    -----
    The cotangent Laplacian at vertex $\mathbf{v}_i$ points toward the
    projection of the vertex into its one-ring plane. These vectors therefore
    approximate the per-vertex normals.

    For a mesh with edges $\mathbf{E}$, the $n \times n$ matrix $\mathbf{L}$
    is defined as[^trimesh-cotangent-laplacian]

    $$
    \mathbf{L}_{ij} =
    \begin{cases}
    -1 & \text{if } i = j \\
    w_{ij} & \text{if } (i, j) \in \mathbf{E} \\
    0 & \text{otherwise}
    \end{cases}
    $$

    with

    $$
    w_{ij} = \frac{\omega_{ij}}
    {\sum_{(i, k) \in \mathbf{E}_{i}} \omega_{ik}}
    $$

    References
    ----------
    [^trimesh-cotangent-laplacian]: Nealen, A., Igarashi, T., Sorkine, O.,
        and Alexa, M. [Laplacian Mesh Optimization](https://igl.ethz.ch/projects/Laplacian-mesh-processing/Laplacian-mesh-optimization/lmo.pdf).

    """
    from scipy.sparse import coo_matrix

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

        if nbrs and W == 0:
            raise ValueError(f"The cotangent weights at vertex {vertex!r} sum to zero.")

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


def trimesh_vertexarea_matrix(mesh: "Mesh") -> "dia_matrix":
    """Compute the diagonal matrix of barycentric vertex areas.

    Parameters
    ----------
    mesh : Mesh
        The triangle mesh data structure.

    Returns
    -------
    scipy.sparse.dia_matrix
        The diagonal barycentric-area matrix. Each triangle contributes one
        third of its area to each incident vertex.

    Examples
    --------
    >>> from compas.datastructures import Mesh
    >>> mesh = Mesh.from_polygons([[[0, 0, 0], [1, 0, 0], [0, 1, 0]]])
    >>> A = trimesh_vertexarea_matrix(mesh)
    >>> A.diagonal().tolist()
    [0.1666, 0.1666, 0.1666]

    """
    from numpy import asarray
    from numpy import bincount
    from numpy import cross
    from numpy import zeros
    from scipy.sparse import spdiags

    from compas.linalg.decompositions import normrow

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
