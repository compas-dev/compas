from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas.geometry.basic import subtract_vectors
from compas.geometry.basic import subtract_vectors_xy
from compas.geometry.basic import cross_vectors
from compas.geometry.basic import cross_vectors_xy
from compas.geometry.basic import length_vector
from compas.geometry.basic import length_vector_xy

from compas.geometry.average import centroid_points


__all__ = [
    'normal_polygon',
    'normal_triangle',
    'normal_triangle_xy',
]


def normal_polygon(polygon, unitized=True):
    """Compute the normal of a polygon defined by a sequence of points.

    Parameters
    ----------
    polygon : list of list
        A list of polygon point coordinates.

    Returns
    -------
    list
        The normal vector.

    Raises
    ------
    ValueError
        If less than three points are provided.

    Notes
    -----
    The points in the list should be unique. For example, the first and last
    point in the list should not be the same.

    """
    p = len(polygon)

    assert p > 2, "At least three points required"

    nx = 0
    ny = 0
    nz = 0

    o = centroid_points(polygon)
    a = polygon[-1]
    oa = subtract_vectors(a, o)

    for i in range(p):
        b = polygon[i]
        ob = subtract_vectors(b, o)
        n = cross_vectors(oa, ob)
        oa = ob

        nx += n[0]
        ny += n[1]
        nz += n[2]

    if not unitized:
        return nx, ny, nz

    l = length_vector([nx, ny, nz])

    return nx / l, ny / l, nz / l


def normal_triangle(triangle, unitized=True):
    """Compute the normal vector of a triangle.

    Parameters
    ----------
    triangle : list of list
        A list of triangle point coordinates.

    Returns
    -------
    list
        The normal vector.

    Raises
    ------
    ValueError
        If the triangle does not have three vertices.

    """
    assert len(triangle) == 3, "Three points are required."
    a, b, c = triangle
    ab = subtract_vectors(b, a)
    ac = subtract_vectors(c, a)
    n  = cross_vectors(ab, ac)
    if not unitized:
        return n
    lvec = length_vector(n)
    return n[0] / lvec, n[1] / lvec, n[2] / lvec


def normal_triangle_xy(triangle, unitized=True):
    """Compute the normal vector of a triangle assumed to lie in the XY plane.

    Parameters
    ----------
    triangle : list of list
        A list of triangle point coordinates.
        Z-coordinates are ignored.

    Returns
    -------
    list
        The normal vector, which is a vector perpendicular to the XY plane.

    Raises
    ------
    ValueError
        If the triangle does not have three vertices.

    """
    a, b, c = triangle
    ab = subtract_vectors_xy(b, a)
    ac = subtract_vectors_xy(c, a)
    n  = cross_vectors_xy(ab, ac)
    if not unitized:
        return n
    lvec = length_vector_xy(n)
    return n[0] / lvec, n[1] / lvec, n[2] / lvec


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":
    
    from compas.geometry import area_polygon
    from compas.geometry import centroid_points
    from compas.plotters import Plotter

    plotter = Plotter(figsize=(10, 7))

    points = [
        [0, 0, 0],
        [1.0, 0, 0],
        [1.0, 1.0, 0],
        [0.5, 0.0, 0],
        [0, 1.0, 0]
    ]
    polygon = points[::-1]

    print(polygon)
    print(area_polygon(polygon))

    n = normal_polygon(polygon, unitized=False)
    print(n)

    if n[2] > 0:
        color = '#ff0000'
    else:
        color = '#0000ff'

    polygons = [{
        'points' : polygon
    }]
    points = [{
        'pos' : centroid_points(polygon),
        'radius' : 0.025,
        'facecolor' : color
    }]

    plotter.draw_polygons(polygons)
    plotter.draw_points(points)

    plotter.show()

