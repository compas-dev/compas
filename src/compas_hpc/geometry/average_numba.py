
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas_hpc.geometry import add_vectors_numba
from compas_hpc.geometry import add_vectors_xy_numba
from compas_hpc.geometry import cross_vectors_numba
from compas_hpc.geometry import dot_vectors_numba
from compas_hpc.geometry import length_vector_numba
from compas_hpc.geometry import length_vector_xy_numba
from compas_hpc.geometry import scale_vector_numba
from compas_hpc.geometry import scale_vector_xy_numba
from compas_hpc.geometry import subtract_vectors_numba
from compas_hpc.geometry import subtract_vectors_xy_numba
from compas_hpc.geometry import sum_vectors_numba

from numba import f8
from numba import i8
from numba import jit

from numpy import array


__all__ = [
    'centroid_points_numba',
    'centroid_points_xy_numba',
    'midpoint_point_point_numba',
    'midpoint_point_point_xy_numba',
    'center_of_mass_polyline_numba',
    'center_of_mass_polyline_xy_numba',
    'center_of_mass_polyhedron_numba',
]


@jit(f8[:](f8[:, :]), nogil=True, nopython=True, parallel=False, cache=True)
def centroid_points_numba(u):

    """ Compute the centroid of a set of points.

    Parameters
    ----------
    u : array
        An array of XYZ coordinates.

    Returns
    -------
    array
        Centroid of the points.

    """

    m = u.shape[0]
    sc = 1. / m
    return scale_vector_numba(sum_vectors_numba(u, axis=0), factor=sc)


@jit(f8[:](f8[:, :]), nogil=True, nopython=True, parallel=False, cache=True)
def centroid_points_xy_numba(u):

    """ Compute the centroid of a set of points lying in the XY plane.

    Parameters
    ----------
    u : array
        An array of XY(Z) coordinates in the XY plane.

    Returns
    -------
    array
        Centroid of the points (Z = 0.0).

    """

    u[:, 2] = 0
    return centroid_points_numba(u)


@jit(f8[:](f8[:], f8[:]), nogil=True, nopython=True, parallel=False, cache=True)
def midpoint_point_point_numba(u, v):

    """ Compute the midpoint of two points.

    Parameters
    ----------
    u : array
        XYZ coordinates of the first point.
    v : array
        XYZ coordinates of the second point.

    Returns
    -------
    array
        XYZ coordinates of the midpoint.

    """

    return scale_vector_numba(add_vectors_numba(u, v), factor=0.5)


@jit(f8[:](f8[:], f8[:]), nogil=True, nopython=True, parallel=False, cache=True)
def midpoint_point_point_xy_numba(u, v):

    """ Compute the midpoint of two points lying in the XY-plane.

    Parameters
    ----------
    u : array
        XY(Z) coordinates of the first point in the XY plane.
    v : array
        XY(Z) coordinates of the second point in the XY plane.

    Returns
    -------
    array
        XYZ (Z = 0.0) coordinates of the midpoint.

    """

    return scale_vector_xy_numba(add_vectors_xy_numba(u, v), factor=0.5)


@jit(f8[:](f8[:, :]), nogil=True, nopython=True, parallel=False, cache=True)
def center_of_mass_polyline_numba(polyline):

    """ Compute the center of mass of polyline edges defined as an array of points.

    Parameters
    ----------
    polyline : array
        XYZ coordinates representing the corners of a polyline (m x 3).

    Returns
    -------
    array
        The XYZ coordinates of the center of mass.

    """

    L = 0
    cx = 0
    cy = 0
    cz = 0
    m = polyline.shape[0]
    ii = list(range(1, m)) + [0]
    for i in range(m):
        p1 = polyline[i, :]
        p2 = polyline[ii[i], :]
        d = length_vector_numba(subtract_vectors_numba(p2, p1))
        cx += 0.5 * d * (p1[0] + p2[0])
        cy += 0.5 * d * (p1[1] + p2[1])
        cz += 0.5 * d * (p1[2] + p2[2])
        L += d
    c = array([cx, cy, cz])
    sc = 1. / L
    return scale_vector_numba(c, factor=sc)


@jit(f8[:](f8[:, :]), nogil=True, nopython=True, parallel=False, cache=True)
def center_of_mass_polyline_xy_numba(polyline):

    """ Compute the center of mass of polyline edges in the XY plane, defined as an array of points.

    Parameters
    ----------
    polyline : array
        XY(Z) coordinates representing the corners of a polyline (m x 3).

    Returns
    -------
    array
        The XY(Z) coordinates of the center of mass.

    """

    L = 0
    cx = 0
    cy = 0
    m = polyline.shape[0]
    ii = list(range(1, m)) + [0]
    for i in range(m):
        p1 = polyline[i, :]
        p2 = polyline[ii[i], :]
        d = length_vector_xy_numba(subtract_vectors_xy_numba(p2, p1))
        cx += 0.5 * d * (p1[0] + p2[0])
        cy += 0.5 * d * (p1[1] + p2[1])
        L += d
    c = array([cx, cy, 0.])
    sc = 1. / L
    return scale_vector_numba(c, factor=sc)


@jit(f8[:](f8[:, :], i8[:, :]), nogil=True, nopython=True, parallel=False, cache=True)
def center_of_mass_polyhedron_numba(vertices, faces):

    """ Compute the center of mass of the edges of a polyhedron.

    Parameters
    ----------
    vertices : array
        XYZ coordinates of the polyhedron vertices (n x 3).
    faces : array
        Indices of triangle faces of the polyhedron (m x 3).

    Return
    ------
    array
        The XYZ coordinates of the polyhedron edges' center of mass.

    """

    m  = faces.shape[0]
    V  = 0.
    x  = 0.
    y  = 0.
    z  = 0.
    ex = array([1., 0., 0.])
    ey = array([0., 1., 0.])
    ez = array([0., 0., 1.])
    ii = [1, 2, 0]

    for i in range(m):
        a = vertices[faces[i, 0]]
        b = vertices[faces[i, 1]]
        c = vertices[faces[i, 2]]
        ab = subtract_vectors_numba(b, a)
        ac = subtract_vectors_numba(c, a)
        n  = cross_vectors_numba(ab, ac)
        V += dot_vectors_numba(a, n)
        nx = dot_vectors_numba(n, ex)
        ny = dot_vectors_numba(n, ey)
        nz = dot_vectors_numba(n, ez)

        for k in range(3):
            ab = add_vectors_numba(vertices[faces[i, k]], vertices[faces[i, ii[k]]])
            x += nx * dot_vectors_numba(ab, ex)**2
            y += ny * dot_vectors_numba(ab, ey)**2
            z += nz * dot_vectors_numba(ab, ez)**2

    if V < 10**(-9):
        V = 0.
        d = 1. / 48.
    else:
        V /= 6.
        d = 1. / 48. / V
    x *= d
    y *= d
    z *= d

    return array([x, y, z])


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    from time import time

    u = array([1., 2., 3.])
    v = array([4., 5., 6.])
    c = array([[0., 0., 1.], [3., 4., 1.], [6., 0., 1.]])

    tic = time()

    for i in range(10**6):

        # a = centroid_points_numba(c)
        # a = centroid_points_xy_numba(c)
        # a = midpoint_point_point_numba(u, v)
        # a = midpoint_point_point_xy_numba(u, v)
        # a = center_of_mass_polyline_numba(c)
        # a = center_of_mass_polyline_xy_numba(c)
        a = center_of_mass_polyhedron_numba(c, array([[0, 1, 2]]))

    print(time() - tic)
    print(a)
