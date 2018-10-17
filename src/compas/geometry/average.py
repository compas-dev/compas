from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas.utilities import window

from compas.geometry.basic import add_vectors
from compas.geometry.basic import subtract_vectors
from compas.geometry.basic import subtract_vectors_xy
from compas.geometry.basic import length_vector
from compas.geometry.basic import length_vector_xy
from compas.geometry.basic import dot_vectors
from compas.geometry.basic import cross_vectors
from compas.geometry.basic import vector_from_points
from compas.geometry.basic import scale_vector
from compas.geometry.distance import distance_point_point


__all__ = [
    'centroid_points',
    'centroid_points_xy',
    'midpoint_point_point',
    'midpoint_point_point_xy',
    'midpoint_line',
    'midpoint_line_xy',
    'center_of_mass_polygon',
    'center_of_mass_polygon_xy',
    'center_of_mass_polyhedron',
    'tween_points',
    'tween_points_distance'
]


def centroid_points(points):
    """Compute the centroid of a set of points.

    Warning
    -------
    Duplicate points are **NOT** removed. If there are duplicates in the
    sequence, they should be there intentionally.

    Parameters
    ----------
    points : sequence
        A sequence of XYZ coordinates.

    Returns
    -------
    list
        XYZ coordinates of the centroid.

    Examples
    --------
    >>> centroid_points()

    """
    p = len(points)
    x, y, z = zip(*points)
    return sum(x) / p, sum(y) / p, sum(z) / p


def centroid_points_xy(points):
    """Compute the centroid of a set of points lying in the XY-plane.

    Warning
    -------
    Duplicate points are **NOT** removed. If there are duplicates in the
    sequence, they should be there intentionally.

    Parameters
    ----------
    points : list of list
        A sequence of points represented by their XY(Z) coordinates.

    Returns
    -------
    list
        XYZ coordinates of the centroid (Z = 0.0).

    Examples
    --------
    >>> centroid_points_xy()

    """
    p = len(points)
    x, y = list(zip(*points))[:2]
    return [sum(x) / p, sum(y) / p, 0.0]


def midpoint_point_point(a, b):
    """Compute the midpoint of two points lying in the XY-plane.

    Parameters
    ----------
    a : sequence of float
        XYZ coordinates of the first point.
    b : sequence of float
        XYZ coordinates of the second point.

    Returns
    -------
    list
        XYZ coordinates of the midpoint.

    """
    return [0.5 * (a[0] + b[0]),
            0.5 * (a[1] + b[1]),
            0.5 * (a[2] + b[2])]


def midpoint_point_point_xy(a, b):
    """Compute the midpoint of two points lying in the XY-plane.

    Parameters
    ----------
    a : sequence of float
        XY(Z) coordinates of the first 2D or 3D point (Z will be ignored).
    b : sequence of float
        XY(Z) coordinates of the second 2D or 3D point (Z will be ignored).

    Returns
    -------
    list
        XYZ coordinates of the midpoint (Z = 0.0).

    """
    return [0.5 * (a[0] + b[0]), 0.5 * (a[1] + b[1]), 0.0]


def midpoint_line(line):
    """Compute the midpoint of a line defined by two points.

    Parameters
    ----------
    line : 2-tuple
        XYZ coordinates of the first point, and XYZ coordinates of the second point.

    Returns
    -------
    list
        XYZ coordinates of the midpoint.

    Examples
    --------
    >>> midpoint_line(([0.0, 0.0, 0.0], [1.0, 0.0, 1.0]))

    """
    return midpoint_point_point(*line)


def midpoint_line_xy(line):
    """Compute the midpoint of a line defined by two points.

    Parameters
    ----------
    line : 2-tuple
        XYZ coordinates of the first point, and XYZ coordinates of the second point.

    Returns
    -------
    list
        XYZ coordinates of the midpoint.

    Examples
    --------
    >>> midpoint_line_xy(([0.0, 0.0, 0.0], [1.0, 0.0, 1.0]))

    """
    return midpoint_point_point_xy(*line)


def center_of_mass_polygon(polygon):
    """Compute the center of mass of a polygon defined as a sequence of points.

    The center of mass of a polygon is the centroid of the midpoints of the edges,
    each weighted by the length of the corresponding edge.

    Parameters
    ----------
    polygon : sequence
        A sequence of XYZ coordinates representing the locations of the corners of a polygon.

    Returns
    -------
    tuple
        The XYZ coordinates of the center of mass.

    Examples
    --------
    >>> points = [(0., 0., 0.), (1., 0., 0.), (0., 10., 0.)]
    >>> center_of_mass_polygon(points)

    """
    L  = 0
    cx = 0
    cy = 0
    cz = 0
    p  = len(polygon)
    for i in range(-1, p - 1):
        p1  = polygon[i]
        p2  = polygon[i + 1]
        d   = length_vector(subtract_vectors(p2, p1))
        cx += 0.5 * d * (p1[0] + p2[0])
        cy += 0.5 * d * (p1[1] + p2[1])
        cz += 0.5 * d * (p1[2] + p2[2])
        L  += d
    cx = cx / L
    cy = cy / L
    cz = cz / L
    return cx, cy, cz


def center_of_mass_polygon_xy(polygon):
    """Compute the center of mass of a polygon defined as a sequence of points lying in the XY-plane.

    The center of mass of a polygon is the centroid of the midpoints of the edges,
    each weighted by the length of the corresponding edge.

    Parameters
    ----------
    polygon : sequence
        A sequence of XY(Z) coordinates of 2D or 3D points (Z will be ignored)
        representing the locations of the corners of a polygon.

    Returns
    -------
    tuple
        The XYZ coordinates of the center of mass (Z = 0.0).

    Examples
    --------
    >>>

    """
    L  = 0
    cx = 0
    cy = 0
    p  = len(polygon)
    for i in range(-1, p - 1):
        p1  = polygon[i]
        p2  = polygon[i + 1]
        d   = length_vector_xy(subtract_vectors_xy(p2, p1))
        cx += 0.5 * d * (p1[0] + p2[0])
        cy += 0.5 * d * (p1[1] + p2[1])
        L  += d
    cx = cx / L
    cy = cy / L
    return cx, cy, 0.0


def center_of_mass_polyhedron(polyhedron):
    """Compute the center of mass of a polyhedron.

    Parameters
    ----------
    polyhedron : tuple
        The coordinates of the vertices,
        and the indices of the vertices forming the faces.

    Returns
    -------
    tuple
        XYZ coordinates of the center of mass.

    Examples
    --------
    >>> from compas.geometry import Polyhedron
    >>> p = Polyhedron.generate(6)
    >>> center_of_mass_polyhedron((p.vertices, p.faces))
    (-4.206480876464043e-17, -4.206480876464043e-17, -4.206480876464043e-17)

    """
    vertices, faces = polyhedron

    V  = 0
    x  = 0.0
    y  = 0.0
    z  = 0.0
    ex = [1.0, 0.0, 0.0]
    ey = [0.0, 1.0, 0.0]
    ez = [0.0, 0.0, 1.0]

    for face in faces:
        if len(face) == 3:
            triangles = [face]
        else:
            centroid = centroid_points([vertices[index] for index in face])
            vertices.append(centroid)
            w = len(vertices) - 1
            triangles = [[u, v, w] for u, v in window(face + face[0:1], 2)]

        for triangle in triangles:
            a  = vertices[triangle[0]]
            b  = vertices[triangle[1]]
            c  = vertices[triangle[2]]
            ab = subtract_vectors(b, a)
            ac = subtract_vectors(c, a)
            n  = cross_vectors(ab, ac)
            V += dot_vectors(a, n)
            nx = dot_vectors(n, ex)
            ny = dot_vectors(n, ey)
            nz = dot_vectors(n, ez)

            for j in (-1, 0, 1):
                ab = add_vectors(vertices[triangle[j]], vertices[triangle[j + 1]])
                x += nx * dot_vectors(ab, ex) ** 2
                y += ny * dot_vectors(ab, ey) ** 2
                z += nz * dot_vectors(ab, ez) ** 2

    if V < 1e-9:
        V = 0.0
        d = 1.0 / 48.0
    else:
        V = V / 6.0
        d = 1.0 / 48.0 / V

    x *= d
    y *= d
    z *= d

    return x, y, z


def tween_points(points1, points2, num):
    """Compute the interpolated points between two sets of points.

    Parameters
    ----------
    points1 : list
        The first set of points
    points2 : list
        The second set of points
    num : int
        The number of interpolated sets to return
    Returns
    -------
    list
        Nested list of points

    """
    tweens = []
    for j in range(num - 1):
        tween = []
        for i in range(len(points1)):
            tween.append(add_vectors(points1[i], scale_vector(vector_from_points(points1[i], points2[i]), 1 / (num / (j + 1)))))
        tweens.append(tween)
    return tweens


def tween_points_distance(points1, points2, dist, index=None):
    """Compute an interpolated set of points between two sets of points, at
    a given distance.

    Parameters
    ----------
    points1 : list
        The first set of points
    points2 : list
        The second set of points
    dist : float
        The distance from the first set to the second at which to compute the
        interpolated set.
    index: int
        The index of the point in the first set from which to calculate the
        distance to the second set. If no value is given, the first point will be used.
    Returns
    -------
    list
        List of points

    """
    if not index:
        index = 0
    d = distance_point_point(points1[index], points2[index])
    scale = float(dist) / d
    tweens = []
    for i in range(len(points1)):
        tweens.append(add_vectors(points1[i], scale_vector(vector_from_points(points1[i], points2[i]), scale)))
    return tweens


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    from compas.geometry import Polyhedron

    p = Polyhedron.generate(6)

    c = center_of_mass_polyhedron((p.vertices, p.faces))

    print(c)
