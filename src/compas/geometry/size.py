from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from math import fabs

from compas.utilities import pairwise

from compas.geometry.basic import subtract_vectors
from compas.geometry.basic import subtract_vectors_xy
from compas.geometry.basic import length_vector
from compas.geometry.basic import length_vector_xy
from compas.geometry.basic import cross_vectors
from compas.geometry.basic import cross_vectors_xy
from compas.geometry.basic import dot_vectors

from compas.geometry.average import centroid_points
from compas.geometry.average import centroid_points_xy

from compas.geometry.normals import normal_triangle
from compas.geometry.normals import normal_triangle_xy


__all__ = [
    'area_polygon',
    'area_polygon_xy',
    'area_triangle',
    'area_triangle_xy',
    'volume_polyhedron',
]


def area_polygon(polygon):
    """Compute the area of a polygon.

    Parameters
    ----------
    polygon : sequence
        The XYZ coordinates of the vertices/corners of the polygon.
        The vertices are assumed to be in order.
        The polygon is assumed to be closed:
        the first and last vertex in the sequence should not be the same.

    Returns
    -------
    float
        The area of the polygon.

    Examples
    --------
    .. plot::
        :include-source:

        from compas.geometry import area_polygon
        from compas.plotters import Plotter

        plotter = Plotter()

        polygon = [
            [0.0, 0.0, 0.0],
            [1.0, 0.0, 0.0],
            [1.0, 1.0, 0.0],
            [0.0, 1.0, 0.0]
        ]

        area_polygon(polygon)

        # 1.0

        plotter.draw_polygons([{'points': polygon}])
        plotter.show()

    .. plot::
        :include-source:

        from compas.geometry import area_polygon
        from compas.plotters import Plotter

        plotter = Plotter()

        polygon = [
            [0.0, 0.0, 0.0],
            [1.0, 0.0, 0.0],
            [1.0, 1.0, 0.0],
            [0.5, 0.0, 0.0],
            [0.0, 1.0, 0.0]
        ]

        area_polygon(polygon)

        # 0.5

        plotter.draw_polygons([{'points': polygon}])
        plotter.show()

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

    return area


def area_polygon_xy(polygon):
    """Compute the area of a polygon lying in the XY-plane.

    Parameters
    ----------
    polygon : sequence
        A sequence of XY(Z) coordinates of 2D or 3D points
        representing the locations of the corners of a polygon.
        The vertices are assumed to be in order. The polygon is assumed to be closed:
        the first and last vertex in the sequence should not be the same.

    Returns
    -------
    float
        The area of the polygon.

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


def area_triangle(triangle):
    """Compute the area of a triangle defined by three points.

    Parameters
    ----------
    triangle : list of list
        XYZ coordinates of the corners of the triangle.

    Returns
    -------
    float
        The area of the triangle.

    """
    return 0.5 * length_vector(normal_triangle(triangle, False))


def area_triangle_xy(triangle):
    """Compute the area of a triangle defined by three points lying in the XY-plane.

    Parameters
    ----------
    triangle : list of list
        XY(Z) coordinates of the corners of the triangle.

    Returns
    -------
    float
        The area of the triangle.

    """
    return 0.5 * length_vector_xy(normal_triangle_xy(triangle, False))


def volume_polyhedron(polyhedron):
    r"""Compute the volume of a polyhedron represented by a closed mesh.

    Parameters
    ----------
    polyhedron : tuple
        The vertices and faces of the polyhedron.

    Returns
    -------
    float
        The volume of the polyhedron.

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

    Warning
    -------
    The volume computed by this funtion is only correct if the polyhedron is convex,
    has planar faces, and is positively oriented (all face normals point outwards).

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
            a  = xyz[u]
            b  = xyz[v]
            c  = xyz[w]
            ab = subtract_vectors(b, a)
            ac = subtract_vectors(c, a)
            n  = cross_vectors(ab, ac)
            V += dot_vectors(a, n)
    return V / 6.


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    from compas.plotters import Plotter
    from compas.geometry import Polyhedron
    from compas.geometry import length_vector
    from compas.geometry import subtract_vectors
    from compas.geometry import centroid_polyhedron

    cube = Polyhedron.generate(6)

    L = length_vector(subtract_vectors(cube.vertices[0], cube.vertices[1]))

    V1 = L * L * L
    V2 = volume_polyhedron(cube)

    print(V1 - V2 <= 1e-6)

    # plotter = Plotter(figsize=(10, 7))

    # polygon = [
    #     [0, 0, 0],
    #     [1.0, 0, 0],
    #     [1.0, 1.0, 0],
    #     [0.5, 0.0, 0],
    #     [0, 1.0, 0]
    # ]

    # print(area_polygon(polygon[::-1]))

    # polygons = [{
    #     'points' : polygon
    # }]

    # plotter.draw_polygons(polygons)

    # plotter.show()

