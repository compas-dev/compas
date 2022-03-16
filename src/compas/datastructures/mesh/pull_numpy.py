from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from numpy import array
from numpy import float64
from numpy import argmin
from numpy import sqrt
from numpy import sum

from scipy.linalg import solve
from scipy.spatial import distance_matrix

from compas.numerical import normalizerow

from compas.geometry import cross_vectors
from compas.geometry import is_ccw_xy
from compas.geometry import is_point_in_triangle


__all__ = [
    'trimesh_pull_points_numpy'
]


def trimesh_pull_points_numpy(mesh, points):
    """Pull points onto a mesh by computing the closest point on the mesh for each of the points.

    Parameters
    ----------
    mesh : :class:`~compas.datastructures.Mesh`
        A mesh data structure.
    points : sequence[[float, float, float] | :class:`~compas.geometry.Point`]
        The input points.

    Returns
    -------
    list[[float, float, float]]
        The points on the mesh.

    Notes
    -----
    It will not be verified that the input mesh is a triangle mesh.
    It will just be treated as if it is...

    """
    # preprocess
    i_k = mesh.index_key()
    fk_fi = {fkey: index for index, fkey in enumerate(mesh.faces())}
    vertices = array(mesh.vertices_attributes('xyz'), dtype=float64).reshape((-1, 3))
    triangles = array([mesh.face_coordinates(fkey) for fkey in mesh.faces()], dtype=float64)
    points = array(points, dtype=float64).reshape((-1, 3))
    closest_vis = argmin(distance_matrix(points, vertices), axis=1)
    # transformation matrices
    # ?
    pulled_points = []
    # pull every point onto the mesh
    for i in range(points.shape[0]):
        point = points[i]
        closest_vi = closest_vis[i]
        closest_vk = i_k[closest_vi]
        closest_tris = [fk_fi[fk] for fk in mesh.vertex_faces(closest_vk, ordered=True) if fk is not None]
        # process the connected triangles
        d, p, c = _find_closest_component(
            point,
            vertices,
            triangles,
            closest_tris,
            closest_vi
        )
        pulled_points.append(p)
    return pulled_points


# ==============================================================================
# helpers
# ==============================================================================


def _is_point_in_edgezone(p, p0, p1):
    n = cross_vectors(p1 - p0, [0, 0, 1.])
    return (is_ccw_xy(p0 - p0, n, p - p0) and
            not is_ccw_xy(p0 - p0, p1 - p0, p - p0) and
            not is_ccw_xy(p1 - p1, n, p - p1))


def _compute_point_on_segment(p, p0, p1):
    a = p1[1] - p0[1]
    b = p0[0] - p1[0]
    c = p1[0] * p0[1] - p1[1] * p0[0]
    r = (b * (b * p[0] - a * p[1]) - a * c) / (a ** 2 + b ** 2)
    s = (a * (-b * p[0] + a * p[1]) - b * c) / (a ** 2 + b ** 2)
    t = 0
    return array([[r, s, t], ])


def _triangle_xform(triangle):
    o = triangle[0]
    u = triangle[1] - o
    v = triangle[2] - o
    w = cross_vectors(u, v)
    v = cross_vectors(w, u)
    A = normalizerow(array([u, v, w])).T
    return o, A


def _find_closest_component(point, vertices, triangles, closest_tris, closest_vi):
    distance = None
    projection = None
    component = None

    for tri in closest_tris:
        # the triangle to process
        triangle = triangles[tri]
        # the local triangle frame
        o, A = _triangle_xform(triangle)
        # local coordinates
        b = point - o
        p = solve(A, b.T).T
        b = triangle - o
        t = solve(A, b.T).T
        # find closest component of triangle
        # compute distance to closest component
        if is_point_in_triangle(p, t):
            p[2] = 0
            xyz = A.dot(p[:, None]).T + o
            distance = 0
            # why to list?
            projection = xyz[0].tolist()
            component = 'face', tri
            break
        if _is_point_in_edgezone(p, t[0], t[1]):
            rst = _compute_point_on_segment(p, t[0], t[1])
            xyz = A.dot(rst.T).T + o
            d = sqrt(sum((rst - p[None, :]) ** 2))
            if distance is None or d < distance:
                distance = d
                # why to list?
                projection = xyz[0].tolist()
                component = 'edge', (None, None)
        elif _is_point_in_edgezone(p, t[1], t[2]):
            rst = _compute_point_on_segment(p, t[1], t[2])
            xyz = A.dot(rst.T).T + o
            d = sqrt(sum((rst - p[None, :]) ** 2))
            if distance is None or d < distance:
                distance = d
                # why to list?
                projection = xyz[0].tolist()
                component = 'edge', (None, None)
        elif _is_point_in_edgezone(p, t[2], t[0]):
            rst = _compute_point_on_segment(p, t[2], t[0])
            xyz = A.dot(rst.T).T + o
            d = sqrt(sum((rst - p[None, :]) ** 2))
            if distance is None or d < distance:
                distance = d
                # why to list?
                projection = xyz[0].tolist()
                component = 'edge', (None, None)
        else:
            xyz = vertices[closest_vi]
            d = sqrt(sum((xyz - point) ** 2))
            if distance is None or d < distance:
                distance = d
                # why to list?
                projection = xyz.tolist()
                component = 'vertex', closest_vi
    return distance, projection, component


# def compute_local_frame(mesh, point):
#     # mesh = mesh.copy()
#     # mesh.unify_cycles()
#     # if not mesh.is_trimesh():
#     #     for fkey in mesh.faces():
#     #         mesh.insert_vertex(fkey)
#     # avoid the previous step
#     i_k          = mesh.index_key()
#     fk_fi        = dict((fkey, index) for index, fkey in mesh.faces_enum())
#     fi_fk        = dict((index, fkey) for index, fkey in mesh.faces_enum())
#     vertices     = array([mesh.vertex_coordinates(key) for key in mesh], dtype=float64).reshape((-1, 3))
#     triangles    = array([mesh.face_coordinates(fkey) for fkey in mesh.face], dtype=float64)
#     closest_vis  = argmin(distance_matrix(array([point, ]), vertices), axis=1)
#     closest_vi   = closest_vis[0]
#     closest_vk   = i_k[closest_vi]
#     closest_tris = [fk_fi[fk] for fk in mesh.vertex_faces(closest_vk, ordered=True) if fk is not None]
#     # closest component
#     cdist, cpoint, ccomp = _find_closest_component(
#         point,
#         vertices,
#         triangles,
#         closest_tris,
#         closest_vi
#     )
#     # compute normal and tangent plane
#     if ccomp[0] == 'face':
#         fkey = fi_fk[ccomp[1]]
#         n    = mesh.face_normal(fkey)
#         return cpoint, n
#     if ccomp[0] == 'vertex':
#         key = i_k[ccomp[1]]
#         n   = mesh.vertex_normal(key)
#         return cpoint, n
#     if ccomp[0] == 'edge':
#         u, v = ccomp[1]
#         n1 = [0, 0, 0]
#         n2 = [0, 0, 0]
#         f1 = mesh.halfedge[u][v]
#         if f1 is not None:
#             n1 = mesh.face_normal(f1)
#         f2 = mesh.halfedge[v][u]
#         if f2 is not None:
#             n2 = mesh.face_normal(f2)
#         n = 0.5 * (n1[0] + n2[0]), 0.5 * (n1[1] + n2[1]), 0.5 * (n1[2] + n2[2])
#         return cpoint, n
#     return None, None


# def compute_tangential_components(mesh, points, residuals):
#     # pre-compute face normals
#     # pre-compute vertex normals
#     # pre-compute edge normals
#     # find closest components
#     # if cc is vertex => use corresponding vertex normal
#     # if cc is edge => use corresponding edge normal
#     # if cc is face => use corresponding face normal
#     # tangent space:
#     # - n
#     # - u = normalizerow(cross(cross(n, r), n))
#     # - t = dot(u, r) * u
#     pass
