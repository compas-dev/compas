from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from math import fabs

from compas.itertools import pairwise

from ._algebra import cross_vectors
from ._algebra import cross_vectors_xy
from ._algebra import dot_vectors
from ._algebra import length_vector
from ._algebra import subtract_vectors
from ._algebra import subtract_vectors_xy
from .centroids import centroid_points
from .centroids import centroid_points_xy
from .normals import normal_triangle
from .normals import normal_triangle_xy


def area_triangle(triangle):
    """Compute the area of a triangle defined by three points.

    Parameters
    ----------
    triangle : [point, point, point] | :class:`compas.geometry.Polygon`
        XYZ coordinates of the corners of the triangle.

    Returns
    -------
    float
        The area of the triangle.

    See Also
    --------
    area_triangle_xy
    area_polygon
    area_polygon_xy

    """
    return 0.5 * length_vector(normal_triangle(triangle, False))


def area_triangle_xy(triangle):
    """Compute the area of a triangle defined by three points lying in the XY-plane.

    Parameters
    ----------
    triangle : [point, point, point] | :class:`compas.geometry.Polygon`
        XY(Z) coordinates of the corners of the triangle.

    Returns
    -------
    float
        The area of the triangle.

    See Also
    --------
    area_triangle
    area_polygon
    area_polygon_xy

    """
    return 0.5 * length_vector(normal_triangle_xy(triangle, False))


def area_polygon(polygon):
    """Compute the area of a polygon.

    Parameters
    ----------
    polygon : sequence[point] | :class:`compas.geometry.Polygon`
        The XYZ coordinates of the vertices/corners of the polygon.
        The vertices are assumed to be in order.
        The polygon is assumed to be closed:
        the first and last vertex in the sequence should not be the same.

    Returns
    -------
    float
        The area of the polygon.

    See Also
    --------
    area_polygon_xy
    area_triangle

    """
    o = centroid_points(polygon)
    a = polygon[-1]
    b = polygon[0]
    oa = subtract_vectors(a, o)
    ob = subtract_vectors(b, o)
    n0 = cross_vectors(oa, ob)
    area = 0.5 * length_vector(n0)
    for i in range(0, len(polygon) - 1):
        oa = ob
        b = polygon[i + 1]
        ob = subtract_vectors(b, o)
        n = cross_vectors(oa, ob)
        if dot_vectors(n, n0) > 0:
            area += 0.5 * length_vector(n)
        else:
            area -= 0.5 * length_vector(n)
    return abs(area)


def area_polygon_xy(polygon):
    """Compute the area of a polygon lying in the XY-plane.

    Parameters
    ----------
    polygon : sequence[point] | :class:`compas.geometry.Polygon`
        A sequence of XY(Z) coordinates of 2D or 3D points
        representing the locations of the corners of a polygon.
        The vertices are assumed to be in order. The polygon is assumed to be closed:
        the first and last vertex in the sequence should not be the same.

    Returns
    -------
    float
        The area of the polygon.

    See Also
    --------
    area_polygon
    area_triangle_xy

    """
    o = centroid_points_xy(polygon)
    u = subtract_vectors_xy(polygon[-1], o)
    v = subtract_vectors_xy(polygon[0], o)
    a = 0.5 * cross_vectors_xy(u, v)[2]
    for i in range(0, len(polygon) - 1):
        u = v
        v = subtract_vectors_xy(polygon[i + 1], o)
        a += 0.5 * cross_vectors_xy(u, v)[2]
    return fabs(a)


def volume_polyhedron(polyhedron):
    r"""Compute the volume of a polyhedron represented by a closed mesh.

    Parameters
    ----------
    polyhedron : tuple[sequence[[float, float, float] | :class:`compas.geometry.Point`], sequence[sequence[int]]]
        The vertices and faces of the polyhedron.

    Returns
    -------
    float
        The volume of the polyhedron.

    Warnings
    --------
    The volume computed by this funtion is only correct if the polyhedron is convex,
    has planar faces, and is positively oriented (all face normals point outwards).

    Notes
    -----
    This implementation is based on the divergence theorem, the fact that the
    *area vector* is constant for each face, and the fact that the area of each
    face can be computed as half the length of the cross product of two adjacent
    edge vectors [1]_.

    .. math::
        :nowrap:

        \begin{align}
            V  = \int_{P} 1
              &= \frac{1}{3} \int_{\partial P} \mathbf{x} \cdot \mathbf{n} \\
              &= \frac{1}{3} \sum_{i=0}^{N-1} \int{A_{i}} a_{i} \cdot n_{i} \\
              &= \frac{1}{6} \sum_{i=0}^{N-1} a_{i} \cdot \hat n_{i}
        \end{align}

    References
    ----------
    .. [1] Nurnberg, R. *Calculating the area and centroid of a polygon in 2d*.
           Available at: http://wwwf.imperial.ac.uk/~rn/centroid.pdf

    """
    xyz, faces = polyhedron

    V = 0
    for vertices in faces:
        if len(vertices) == 3:
            triangles = [vertices]
        else:
            centroid = centroid_points([xyz[i] for i in vertices])
            i = len(xyz)
            xyz.append(centroid)
            triangles = []
            for u, v in pairwise(vertices + vertices[0:1]):
                triangles.append([i, u, v])

        for u, v, w in triangles:
            a = xyz[u]
            b = xyz[v]
            c = xyz[w]
            ab = subtract_vectors(b, a)
            ac = subtract_vectors(c, a)
            n = cross_vectors(ab, ac)
            V += dot_vectors(a, n)
    return V / 6.0
