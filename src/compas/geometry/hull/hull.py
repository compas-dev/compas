from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas.geometry import cross_vectors
from compas.geometry import subtract_vectors
from compas.geometry import dot_vectors
from compas.geometry import cross_vectors_xy


__all__ = [
    'convex_hull',
    'convex_hull_xy',
]


def convex_hull(points):
    """Construct convex hull for a set of points.

    Parameters
    ----------
    points : list
        A sequence of XYZ coordinates.

    Returns
    -------
    list
        The triangular faces of the convex hull as lists of vertex indices
        referring to the original point coordinates.

    Notes
    -----
    This algorithm is based on [1]_. Note that is not optimized and relatively
    slow on large sets of points. For a more optimized version of this algorithm,
    see [2]_.

    References
    ----------
    .. [1] GitHubGist. *Convex Hull*.
           Available at: https://gist.github.com/anonymous/5184ba0bcab21d3dd19781efd3aae543
    .. [2] Thomas Diewald. *Convex Hull 3D - Quickhull Algorithm*.
           Available at: https://web.archive.org/web/20180106161310/http://thomasdiewald.com/blog/?p=1888

    Examples
    --------
    >>>

    """
    def _normal_face(face):
        u = subtract_vectors(points[face[1]], points[face[0]])
        v = subtract_vectors(points[face[-1]], points[face[0]])
        return cross_vectors(u, v)

    def _seen(face, p):
        normal = _normal_face(face)
        vec = subtract_vectors(points[p], points[face[0]])
        return (dot_vectors(normal, vec) >= 0)

    def _bdry(faces):
        bdry_fw = set([(face[i - 1], face[i]) for face in faces for i in range(len(face))])
        bdry_bk = set([(face[i], face[i - 1]) for face in faces for i in range(len(face))])
        return bdry_fw - bdry_bk

    def _add_point(hull, p):
        seen_faces = [face for face in hull if _seen(face, p)]

        if len(seen_faces) == len(hull):
            # if can see all faces, unsee ones looking "down"
            normal = _normal_face(seen_faces[0])
            seen_faces = [face for face in seen_faces if dot_vectors(_normal_face(face), normal) > 0]

        for face in seen_faces:
            hull.remove(face)

        for edge in _bdry(seen_faces):
            hull.append([edge[0], edge[1], p])

    hull = [[0, 1, 2], [0, 2, 1]]
    for i in range(3, len(points)):
        _add_point(hull, i)
    return hull


def convex_hull_xy(points, strict=False):
    """Computes the convex hull of a set of 2D points.

    Parameters
    ----------
    points : list
        XY(Z) coordinates of the points.

    Returns
    -------
    list
        XY(Z) coordinates of vertices of the convex hull in counter-clockwise order,
        starting from the vertex with the lexicographically smallest coordinates.

    Notes
    -----
    Implements Andrew's monotone chain algorithm [1]_. O(n log n) complexity.

    References
    ----------
    .. [1] Wiki Books. *Algorithm Implementation/Geometry/Convex hull/Monotone chain*.
           Available at: https://en.wikibooks.org/wiki/Algorithm_Implementation/Geometry/Convex_hull/Monotone_chain.

    Examples
    --------
    >>>

    """
    def cross(o, a, b):
        u = subtract_vectors(a, o)
        v = subtract_vectors(b, o)
        return cross_vectors_xy(u, v)[2]

    # Sort the points lexicographically (tuples are compared lexicographically).
    # Remove duplicates to detect the case we have just one unique point.
    points = sorted(set(map(tuple, points)))

    # Boring case: no points or a single point, possibly repeated multiple times.
    if len(points) <= 1:
        return points

    # Build lower hull
    lower = []
    for p in points:
        if strict:
            while len(lower) >= 2 and cross(lower[-2], lower[-1], p) < 0:
                lower.pop()
        else:
            while len(lower) >= 2 and cross(lower[-2], lower[-1], p) <= 0:
                lower.pop()
        lower.append(p)

    # Build upper hull
    upper = []
    for p in reversed(points):
        if strict:
            while len(upper) >= 2 and cross(upper[-2], upper[-1], p) < 0:
                upper.pop()
        else:
            while len(upper) >= 2 and cross(upper[-2], upper[-1], p) <= 0:
                upper.pop()
        upper.append(p)

    # Concatenation of the lower and upper hulls gives the convex hull.
    # Last point of each list is omitted because it is repeated at the beginning of the other list.
    return lower[:-1] + upper[:-1]


# ==============================================================================
# Main
# ==============================================================================


if __name__ == "__main__":

    # import random
    # from compas.utilities import flatten
    # from compas.datastructures import Mesh
    # from compas_viewers import MeshViewer
    # from compas.topology import unify_cycles

    # radius = 5
    # origin = (0., 0., 0.)
    # count = 0
    # points = []

    # while count < 1000:
    #     x = (random.random() - 0.5) * radius * 2
    #     y = (random.random() - 0.5) * radius * 2
    #     z = (random.random() - 0.5) * radius * 2
    #     pt = x, y, z

    #     if distance_point_point(origin, pt) <= radius:
    #         points.append(pt)
    #         count += 1

    # faces = convex_hull(points)
    # vertices = list(set(flatten(faces)))

    # i_index = {i: index for index, i in enumerate(vertices)}

    # vertices = [points[index] for index in vertices]
    # faces = [[i_index[i] for i in face] for face in faces]
    # faces = unify_cycles(vertices, faces)

    # mesh = Mesh.from_vertices_and_faces(vertices, faces)

    # viewer = MeshViewer()
    # viewer.mesh = mesh
    # viewer.show()

    import doctest
    doctest.testmod(globs=globals())
