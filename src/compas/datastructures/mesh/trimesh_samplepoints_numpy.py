from numpy import array
from numpy.random import choice
from numpy.random import rand
from numpy import sqrt
from numpy import float64
from numpy import cross
from numpy.linalg import norm
from numpy import clip
from numpy import finfo


__all__ = [
    'trimesh_samplepoints_numpy',
]


def trimesh_samplepoints_numpy(mesh, num_points=1000, return_normals=False):
    """Compute sample points on a triangle mesh surface.

    Parameters
    ----------
    mesh : :class:`~compas.datastructures.Mesh`
        A triangle mesh data structure.
    num_points : int, optional
        The number of sample points.
    return_normals : bool, optional
        If True, return the normals in addition to the sample points.

    Returns
    -------
    ndarray | tuple[ndarray, ndarray]
        If `return_normals` is False, a numpy ndarray representing sampled points with dim = [num_points, 3].
        If `return_normals` is True, the sample points and the normals.

    References
    ----------
    .. [1] Barycentric coordinate system, Available at https://en.wikipedia.org/wiki/Barycentric_coordinate_system
    .. [2] Efficient barycentric point sampling on meshes, arXiv:1708.07559

    Examples
    --------
    Make a triangle mesh.

    >>> from compas.datastructures import Mesh
    >>> hypar = Mesh.from_obj(compas.get('hypar.obj'))
    >>> hypar.is_trimesh()
    False
    >>> hypar.quads_to_triangles()

    Compute sample points.

    >>> samples_pts, pts_normals = trimesh_samplepoints_numpy(hypar, 1000, True)
    >>> # the x,y,z of sample points would be the following
    >>> x, y, z = samples_pts[:,0], samples_pts[:,1], samples_pts[:,2]
    >>> # the sample points added normal vector would be the following
    >>> X, Y, Z = x + pts_normals[:,0] , y + pts_normals[:,1] , z + pts_normals[:,2]

    """
    if mesh.is_empty():
        raise ValueError("Mesh is empty.")
    if not mesh.is_trimesh():
        raise ValueError("Mesh is not trimesh.")
    if not mesh.is_valid():
        raise ValueError("Mesh is invalid.")

    # (1)  Prepare data for computing
    key_index = mesh.key_index()
    vertices = mesh.vertices_attributes('xyz')
    faces = [[key_index[key] for key in mesh.face_vertices(fkey)] for fkey in mesh.faces()]
    V = array(vertices, dtype=float64)
    F = array(faces, dtype=int)

    e01 = V[F[:, 1]] - V[F[:, 0]]
    e12 = V[F[:, 2]] - V[F[:, 1]]

    normal = cross(e01, e12)
    area_list = 0.5 * norm(normal, axis=1)
    area_list_norm = area_list / area_list.sum()

    # (2) Sample num_points of times on a mesh face regarding its weight of area
    faces_idx = list(range(mesh.number_of_faces()))
    samples_faces_idx = choice(faces_idx, num_points, p=area_list_norm)

    # (3) Barycentric Coordinate for Surface Sampling
    faces_vertices = V[F]
    v0, v1, v2 = faces_vertices[:, 0], faces_vertices[:, 1], faces_vertices[:, 2]
    r1_r2 = rand(2, num_points)
    r1, r2 = r1_r2[0], r1_r2[1]  # r1, r2 uniformly distributed from 0 to 1
    r1_sqrt = sqrt(r1)
    w0 = 1.0 - r1_sqrt
    w1 = r1_sqrt * (1.0 - r2)
    w2 = r1_sqrt * r2
    a = v0[samples_faces_idx]
    b = v1[samples_faces_idx]
    c = v2[samples_faces_idx]

    # (4) return sample points in the format of ndarray
    samples_points = w0[:, None] * a + w1[:, None] * b + w2[:, None] * c

    # (5) (if True) Return the normal vector of the sampled points
    if return_normals:

        samples_points_normals = cross((v1 - v0), (v2 - v1), axis=1)
        samples_points_normals_norm = norm(samples_points_normals, ord=2, axis=1, keepdims=True)
        samples_points_normals = samples_points_normals / samples_points_normals_norm
        samples_points_normals = clip(samples_points_normals, a_min=finfo(float64).eps, a_max=None)
        samples_points_normals = samples_points_normals[samples_faces_idx]

        return samples_points, samples_points_normals

    return samples_points
