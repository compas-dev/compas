from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from math import fabs

from compas.itertools import pairwise

from ._algebra import add_vectors
from ._algebra import cross_vectors
from ._algebra import cross_vectors_xy
from ._algebra import dot_vectors
from ._algebra import length_vector
from ._algebra import length_vector_xy
from ._algebra import scale_vector
from ._algebra import subtract_vectors
from ._algebra import subtract_vectors_xy
from ._algebra import sum_vectors


def midpoint_point_point(a, b):
    """Compute the midpoint of two points.

    Parameters
    ----------
    a : [float, float, float] | :class:`compas.geometry.Point`
        XYZ coordinates of the first point.
    b : [float, float, float] | :class:`compas.geometry.Point`
        XYZ coordinates of the second point.

    Returns
    -------
    [float, float, float]
        XYZ coordinates of the midpoint.

    """
    return [0.5 * (a[0] + b[0]), 0.5 * (a[1] + b[1]), 0.5 * (a[2] + b[2])]


def midpoint_point_point_xy(a, b):
    """Compute the midpoint of two points lying in the XY-plane.

    Parameters
    ----------
    a : [float, float] or [float, float, float] | :class:`compas.geometry.Point`
        XY(Z) coordinates of the first 2D or 3D point (Z will be ignored).
    b : [float, float] or [float, float, float] | :class:`compas.geometry.Point`
        XY(Z) coordinates of the second 2D or 3D point (Z will be ignored).

    Returns
    -------
    [float, float, 0.0]
        XYZ coordinates of the midpoint in the XY plane.
    """
    return [0.5 * (a[0] + b[0]), 0.5 * (a[1] + b[1]), 0.0]


def midpoint_line(line):
    """Compute the midpoint of a line defined by two points.

    Parameters
    ----------
    line : [point, point] | :class:`compas.geometry.Line`
        XYZ coordinates of the first point, and XYZ coordinates of the second point.

    Returns
    -------
    [float, float, float]
        XYZ coordinates of the midpoint.

    Examples
    --------
    >>> midpoint_line(([0.0, 0.0, 0.0], [1.0, 0.0, 1.0]))
    [0.5, 0.0, 0.5]
    """
    return midpoint_point_point(*line)


def midpoint_line_xy(line):
    """Compute the midpoint of a line defined by two points.

    Parameters
    ----------
    line : [point, point] | :class:`compas.geometry.Line`
        XYZ coordinates of the first point, and XYZ coordinates of the second point.

    Returns
    -------
    [float, float, 0.0]
        XYZ coordinates of the midpoint in the XY plane.

    Examples
    --------
    >>> midpoint_line_xy(([0.0, 0.0, 0.0], [1.0, 0.0, 1.0]))
    [0.5, 0.0, 0.0]
    """
    return midpoint_point_point_xy(*line)


def centroid_points(points):
    """Compute the centroid of a set of points.

    Parameters
    ----------
    points : sequence[[float, float, float] | :class:`compas.geometry.Point`]
        A sequence of XYZ coordinates.

    Returns
    -------
    [float, float, float]
        XYZ coordinates of the centroid.

    Warnings
    --------
    Duplicate points are **NOT** removed. If there are duplicates in the
    sequence, they should be there intentionally.

    Examples
    --------
    >>> points = [[0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [1.0, 1.0, 0.0], [0.0, 1.0, 0.0]]
    >>> centroid_points(points)
    [0.5, 0.5, 0.0]
    """
    p = len(points)
    x, y, z = zip(*points)
    return [sum(x) / p, sum(y) / p, sum(z) / p]


def centroid_points_weighted(points, weights):
    """Compute the weighted centroid of a set of points. The weights can be any between minus and plus infinity.

    Parameters
    ----------
    points : sequence[[float, float, float] | :class:`compas.geometry.Point`]
        A list of point coordinates.
    weights : sequence[float]
        A list of weight floats.

    Returns
    -------
    [float, float, float]
        The coordinates of the weighted centroid.
    """
    vectors = [scale_vector(point, weight) for point, weight in zip(points, weights)]
    vector = scale_vector(sum_vectors(vectors), 1.0 / sum(weights))
    return vector


def centroid_points_xy(points):
    """Compute the centroid of a set of points lying in the XY-plane.

    Parameters
    ----------
    points : sequence[[float, float] or [float, float, float] | :class:`compas.geometry.Point`]
        A sequence of points represented by their XY(Z) coordinates.

    Returns
    -------
    [float, float, 0.0]
        XYZ coordinates of the centroid in the XY plane.

    Warnings
    --------
    Duplicate points are **NOT** removed. If there are duplicates in the
    sequence, they should be there intentionally.

    Examples
    --------
    >>> points = [[0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [1.0, 1.0, 0.0], [0.0, 1.0, 0.0]]
    >>> centroid_points_xy(points)
    [0.5, 0.5, 0.0]
    """
    p = len(points)
    x, y = list(zip(*points))[:2]
    return [sum(x) / p, sum(y) / p, 0.0]


def centroid_polygon(polygon):
    r"""Compute the centroid of the surface of a polygon.

    Parameters
    ----------
    polygon : sequence[[float, float, float] | :class:`compas.geometry.Point`]
        A sequence of polygon point coordinates.

    Returns
    -------
    [float, float, float]
        The XYZ coordinates of the centroid.

    Raises
    ------
    ValueError
        If the polygon has less than three points.

    Warnings
    --------
    The polygon need not be convex.

    The polygon need not be flat. However, it is unclear what the meaning of the
    centroid is in that case.

    The polygon may be self-intersecting. However, it is unclear what the meaning
    of the centroid is in that case.

    Notes
    -----
    The centroid is the centre of gravity of the polygon surface if mass would be
    uniformly distributed over it.

    It is calculated by triangulating the polygon surface with respect to the centroid
    of the polygon vertices, and then computing the centroid of the centroids of
    the individual triangles, weighted by the corresponding triangle area in
    proportion to the total surface area.

    .. math::

        c_x = \frac{1}{A} \sum_{i=1}^{N} A_i \cdot c_{x,i}
        c_y = \frac{1}{A} \sum_{i=1}^{N} A_i \cdot c_{y,i}
        c_z = \frac{1}{A} \sum_{i=1}^{N} A_i \cdot c_{z,i}

    Examples
    --------
    >>> polygon = [[0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [1.0, 1.0, 0.0], [0.0, 1.0, 0.0]]
    >>> centroid_polygon(polygon)
    [0.5, 0.5, 0.0]

    """
    p = len(polygon)

    if p < 3:
        raise ValueError("At least three points required.")

    if p == 3:
        return centroid_points(polygon)

    o = centroid_points(polygon)
    a = polygon[-1]
    b = polygon[0]
    oa = subtract_vectors(a, o)
    ob = subtract_vectors(b, o)
    n0 = cross_vectors(oa, ob)

    x, y, z = centroid_points([o, a, b])
    a2 = length_vector(n0)

    A2 = a2
    cx = a2 * x
    cy = a2 * y
    cz = a2 * z

    for i in range(1, p):
        a = b
        b = polygon[i]

        oa = ob
        ob = subtract_vectors(b, o)

        n = cross_vectors(oa, ob)
        x, y, z = centroid_points([o, a, b])

        if dot_vectors(n, n0) > 0:
            a2 = length_vector(n)
        else:
            a2 = -length_vector(n)

        A2 += a2
        cx += a2 * x
        cy += a2 * y
        cz += a2 * z

    if A2 == 0:
        return polygon[0]

    return [cx / A2, cy / A2, cz / A2]


def centroid_polygon_xy(polygon):
    r"""Compute the centroid of the surface of a polygon projected to the XY plane.

    Parameters
    ----------
    polygon : sequence[[float, float] or [float, float, float] | :class:`compas.geometry.Point`]
        A sequence of polygon point XY(Z) coordinates.
        The Z coordinates are ignored.

    Returns
    -------
    [float, float, 0.0]
        The XYZ coordinates of the centroid in the XY plane.

    Raises
    ------
    ValueError
        If the polygon has less than three points.

    Warnings
    --------
    The polygon need not be convex.

    The polygon may be self-intersecting. However, it is unclear what the meaning
    of the centroid is in that case.

    Notes
    -----
    The centroid is the centre of gravity of the polygon surface if mass would be
    uniformly distributed over it.

    It is calculated by triangulating the polygon surface with respect to the centroid
    of the polygon vertices, and then computing the centroid of the centroids of
    the individual triangles, weighted by the corresponding triangle area in
    proportion to the total surface area.

    .. math::

        c_x = \frac{1}{A} \sum_{i=1}^{N} A_i \cdot c_{x,i}
        c_y = \frac{1}{A} \sum_{i=1}^{N} A_i \cdot c_{y,i}
        c_z = 0

    Examples
    --------
    >>> polygon = [[0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [1.0, 1.0, 0.0], [0.0, 1.0, 0.0]]
    >>> centroid_polygon_xy(polygon)
    [0.5, 0.5, 0.0]

    """
    p = len(polygon)

    if p < 3:
        raise ValueError("At least three points required")

    if p == 3:
        return centroid_points_xy(polygon)

    o = centroid_points_xy(polygon)
    a = polygon[-1]
    b = polygon[0]
    oa = subtract_vectors_xy(a, o)
    ob = subtract_vectors_xy(b, o)
    n0 = cross_vectors_xy(oa, ob)

    x, y, z = centroid_points_xy([o, a, b])
    a2 = fabs(n0[2])

    A2 = a2
    cx = a2 * x
    cy = a2 * y

    for i in range(1, p):
        a = b
        b = polygon[i]

        oa = ob
        ob = subtract_vectors_xy(b, o)

        n = cross_vectors_xy(oa, ob)
        x, y, z = centroid_points_xy([o, a, b])

        if n[2] * n0[2] > 0:
            a2 = fabs(n[2])
        else:
            a2 = -fabs(n[2])

        A2 += a2
        cx += a2 * x
        cy += a2 * y

    return [cx / A2, cy / A2, 0.0]


def centroid_polygon_vertices(polygon):
    """Compute the centroid of the vertices of a polygon.

    Parameters
    ----------
    polygon : sequence[[float, float, float] | :class:`compas.geometry.Point`]
        A sequence of polygon point coordinates.

    Returns
    -------
    [float, float, float]
        The XYZ coordinates of the centroid.

    """
    return centroid_points(polygon)


def centroid_polygon_vertices_xy(polygon):
    """Compute the centroid of the vertices of a polygon projected to the XY plane.

    Parameters
    ----------
    polygon : sequence[[float, float] or [float, float, float] | :class:`compas.geometry.Point`]
        A sequence of polygon point coordinates.
        The Z coordinates will be ignored.

    Returns
    -------
    [float, float, 0.0]
        The XYZ coordinates of the centroid in the XY plane.

    """
    return centroid_points_xy(polygon)


def centroid_polygon_edges(polygon):
    """Compute the centroid of the edges of a polygon.

    Parameters
    ----------
    polygon : sequence[[float, float, float] | :class:`compas.geometry.Point`]
        A sequence of polygon point coordinates.

    Returns
    -------
    [float, float, float]
        The XYZ coordinates of the centroid.

    Notes
    -----
    The centroid of the edges is the centroid of the midpoints of the edges, with
    each midpoint weighted by the length of the corresponding edge proportional
    to the total length of the boundary.
    """
    L = 0
    cx = 0
    cy = 0
    cz = 0
    p = len(polygon)
    for i in range(-1, p - 1):
        p1 = polygon[i]
        p2 = polygon[i + 1]
        d = length_vector(subtract_vectors(p2, p1))
        cx += 0.5 * d * (p1[0] + p2[0])
        cy += 0.5 * d * (p1[1] + p2[1])
        cz += 0.5 * d * (p1[2] + p2[2])
        L += d
    return [cx / L, cy / L, cz / L]


def centroid_polygon_edges_xy(polygon):
    """Compute the centroid of the edges of a polygon prohected to the XY plane.

    Parameters
    ----------
    polygon : sequence[[float, float] or [float, float, float] | :class:`compas.geometry.Point`]
        A sequence of polygon point coordinates.
        The Z coordinates will be ignored.

    Returns
    -------
    [float, float, 0.0]
        The XYZ coordinates of the centroid in the XY plane.

    Notes
    -----
    The centroid of the edges is the centroid of the midpoints of the edges, with
    each midpoint weighted by the length of the corresponding edge proportional
    to the total length of the boundary.
    """
    L = 0
    cx = 0
    cy = 0
    p = len(polygon)
    for i in range(-1, p - 1):
        p1 = polygon[i]
        p2 = polygon[i + 1]
        d = length_vector_xy(subtract_vectors_xy(p2, p1))
        cx += 0.5 * d * (p1[0] + p2[0])
        cy += 0.5 * d * (p1[1] + p2[1])
        L += d
    return [cx / L, cy / L, 0.0]


def centroid_polyhedron(polyhedron):
    """Compute the center of mass of a polyhedron.

    Parameters
    ----------
    polyhedron : tuple[sequence[[float, float, float] | :class:`compas.geometry.Point`], sequence[sequence[int]]]
        The coordinates of the vertices,
        and the indices of the vertices forming the faces.

    Returns
    -------
    [float, float, float]
        XYZ coordinates of the center of mass.

    Warnings
    --------
    This function assumes that the vertex cycles of the faces are such that the
    face normals are consistently pointing outwards, resulting in a *positive*
    polyhedron.

    Examples
    --------
    >>> from compas.geometry import Polyhedron
    >>> p = Polyhedron.from_platonicsolid(6)
    >>> centroid_polyhedron(p)
    [0.0, 0.0, 0.0]
    """
    vertices, faces = polyhedron

    V = 0
    x = 0.0
    y = 0.0
    z = 0.0
    ex = [1.0, 0.0, 0.0]
    ey = [0.0, 1.0, 0.0]
    ez = [0.0, 0.0, 1.0]

    for face in faces:
        if len(face) == 3:
            triangles = [face]
        else:
            centroid = centroid_points([vertices[index] for index in face])
            w = len(vertices)
            vertices.append(centroid)
            triangles = [[w, u, v] for u, v in pairwise(face + face[0:1])]

        for triangle in triangles:
            a = vertices[triangle[0]]
            b = vertices[triangle[1]]
            c = vertices[triangle[2]]
            ab = subtract_vectors(b, a)
            ac = subtract_vectors(c, a)
            n = cross_vectors(ab, ac)
            V += dot_vectors(a, n)

            nx = dot_vectors(n, ex)
            ny = dot_vectors(n, ey)
            nz = dot_vectors(n, ez)

            ab = add_vectors(a, b)
            bc = add_vectors(b, c)
            ca = add_vectors(c, a)

            ab_x2 = dot_vectors(ab, ex) ** 2
            bc_x2 = dot_vectors(bc, ex) ** 2
            ca_x2 = dot_vectors(ca, ex) ** 2

            x += nx * (ab_x2 + bc_x2 + ca_x2)

            ab_y2 = dot_vectors(ab, ey) ** 2
            bc_y2 = dot_vectors(bc, ey) ** 2
            ca_y2 = dot_vectors(ca, ey) ** 2

            y += ny * (ab_y2 + bc_y2 + ca_y2)

            ab_z2 = dot_vectors(ab, ez) ** 2
            bc_z2 = dot_vectors(bc, ez) ** 2
            ca_z2 = dot_vectors(ca, ez) ** 2

            z += nz * (ab_z2 + bc_z2 + ca_z2)

            # for j in (-1, 0, 1):
            #     ab = add_vectors(vertices[triangle[j]], vertices[triangle[j + 1]])
            #     x += nx * dot_vectors(ab, ex) ** 2
            #     y += ny * dot_vectors(ab, ey) ** 2
            #     z += nz * dot_vectors(ab, ez) ** 2

    V = V / 6.0

    if V < 1e-9:
        d = 1.0 / (2 * 24)
    else:
        d = 1.0 / (2 * 24 * V)

    x *= d
    y *= d
    z *= d

    return [x, y, z]
