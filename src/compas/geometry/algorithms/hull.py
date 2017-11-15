from __future__ import print_function
from __future__ import absolute_import

from compas.geometry.basic import cross_vectors
from compas.geometry.basic import subtract_vectors
from compas.geometry.basic import dot_vectors
from compas.geometry.basic import cross_vectors_xy

from compas.geometry.distance import distance_point_point


__author__     = ['Matthias Rippmann <rippmann@ethz.ch>']
__copyright__  = 'Copyright 2014, Block Research Group - ETH Zurich'
__license__    = 'MIT License'
__email__      = '<rippmannt@ethz.ch>'


__all__ = [
    'convex_hull',
    'convex_hull_xy',
    'convex_hull_numpy',
    'convex_hull_xy_numpy',
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

    References
    ----------
    * https://gist.github.com/anonymous/5184ba0bcab21d3dd19781efd3aae543

    Note
    ----
    The algorithm is not optimized and relatively slow on large sets of points.
    See here for a more optimized version of this algorithm:
    http://thomasdiewald.com/blog/?p=1888

    Examples
    --------
    .. code-block:: python

        import math
        import random

        from compas.geometry import distance_point_point
        from compas.cad.rhino.helpers.mesh import draw_mesh
        from compas.datastructures.mesh import Mesh

        radius = 5
        origin = (0., 0., 0.)
        count = 0
        points = []
        while count < 1000:
            x = (random.random() - 0.5) * radius * 2
            y = (random.random() - 0.5) * radius * 2
            z = (random.random() - 0.5) * radius * 2
            pt = x, y, z
            if distance_point_point(origin, pt) <= radius:
                points.append(pt)
                count += 1

        faces =  convex_hull(points)

        mesh = Mesh.from_vertices_and_faces(points, faces)

        draw_mesh(mesh,
                    show_faces = True,
                    show_vertices = False,
                    show_edges = False)

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


def convex_hull_xy(points):
    """Computes the convex hull of a set of 2D points.

    Note
    ----
    Implements Andrew's monotone chain algorithm. O(n log n) complexity.

    Warning
    -------
    This implementation needs to be checked as it seems to use sets incorrectly.

    Parameters
    ----------
    points : list
        XY(Z) coordinates of the points.

    Returns
    -------
    list
        XY(Z) coordinates of vertices of the convex hull in counter-clockwise order,
        starting from the vertex with the lexicographically smallest coordinates.

    References
    ----------
    * https://en.wikibooks.org/wiki/Algorithm_Implementation/Geometry/Convex_hull/Monotone_chain

    """

    # Sort the points lexicographically (tuples are compared lexicographically).
    # Remove duplicates to detect the case we have just one unique point.
    points = sorted(set(points))

    # Boring case: no points or a single point, possibly repeated multiple times.
    if len(points) <= 1:
        return points

    # Build lower hull
    lower = []
    for p in points:
        while len(lower) >= 2 and cross_vectors_xy(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)

    # Build upper hull
    upper = []
    for p in reversed(points):
        while len(upper) >= 2 and cross_vectors_xy(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)

    # Concatenation of the lower and upper hulls gives the convex hull.
    # Last point of each list is omitted because it is repeated at the beginning of the other list.
    return lower[:-1] + upper[:-1]


def convex_hull_numpy(points):
    """Compute the convex hull of a set of points.

    Parameters
    ----------
    points : list
        XYZ coordinates of the points.

    Returns
    -------
    tuple
        Indices of the points on the hull.
        Faces of the hull.

    Warning
    -------
    This function requires Numpy ands Scipy.

    Example
    -------
    .. code-block:: python

        #

    """
    from numpy import asarray
    from scipy.spatial import ConvexHull

    points = asarray(points)
    n, dim = points.shape

    assert 2 < dim, "The point coordinates should be at least 3D: %i" % dim

    points = points[:, :3]
    hull = ConvexHull(points)
    return hull.vertices, hull.simplices


def convex_hull_xy_numpy(points):
    """Compute the convex hull of a set of points in the XY plane.

    Warning
    -------
    This function requires Numpy ands Scipy.

    Parameters
    ----------
    points : list
        XY(Z) coordinates of the points.

    Returns
    -------
    tuple
        Indices of the points on the hull.
        Faces of the hull.

    Example
    -------
    .. code-block:: python

        #

    """
    from numpy import asarray
    # from numpy import hstack
    # from numpy import zeros
    from scipy.spatial import ConvexHull

    points = asarray(points)
    n, dim = points.shape

    assert 1 < dim, "The point coordinates should be at least 2D: %i" % dim

    points = points[:, :2]
    hull = ConvexHull(points)
    # temp = zeros((hull.vertices.shape[0], 1))
    # temp[:, :-1] = points[hull.vertices]
    # return temp
    return hull.vertices, hull.simplices


# ==============================================================================
# Testing
# ==============================================================================


if __name__ == "__main__":

    # todo: distinguish between vertices of hull and internal vertices

    import random

    from compas.datastructures import Mesh
    from compas.viewers import MeshViewer

    radius = 5
    origin = (0., 0., 0.)
    count = 0
    points = []

    while count < 1000:
        x = (random.random() - 0.5) * radius * 2
        y = (random.random() - 0.5) * radius * 2
        z = (random.random() - 0.5) * radius * 2
        pt = x, y, z
        if distance_point_point(origin, pt) <= radius:
            points.append(pt)
            count += 1

    faces = convex_hull(points)

    mesh = Mesh.from_vertices_and_faces(points, faces)

    viewer = MeshViewer(mesh)

    viewer.setup()
    viewer.show()
