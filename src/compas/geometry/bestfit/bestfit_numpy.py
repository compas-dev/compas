from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from numpy import asarray
from numpy import sqrt
from numpy import mean
from numpy import zeros
from numpy.linalg import lstsq
from scipy.optimize import leastsq

from compas.geometry import world_to_local_coordinates_numpy
from compas.geometry import local_to_world_coordinates_numpy
from compas.numerical import pca_numpy


__all__ = [
    'bestfit_plane_numpy',
    'bestfit_frame_numpy',
    'bestfit_circle_numpy',
    'bestfit_sphere_numpy',
]


def bestfit_plane_numpy(points):
    """Fit a plane through more than three (non-coplanar) points.

    Parameters
    ----------
    points : list
        XYZ coordinates of the points.

    Returns
    -------
    tuple
        A point on the plane, and the normal vector.

    Examples
    --------
    >>>

    """
    o, uvw, _ = pca_numpy(points)
    return o, uvw[2]


def bestfit_frame_numpy(points):
    """Fit a frame to a set of points.

    Parameters
    ----------
    points : list
        XYZ coordinates of the points.

    Returns
    -------
    3-tuple
        The frame origin, and the local X and Y axes.

    Examples
    --------
    >>>

    """
    o, uvw, _ = pca_numpy(points)
    return o, uvw[0], uvw[1]


def bestfit_circle_numpy(points):
    """Fit a circle through a set of points.

    Parameters
    ----------
    points : list
        XYZ coordinates of the points.

    Returns
    -------
    tuple
        XYZ coordinates of the center of the circle, the normal vector of the
        local frame, and the radius of the circle.

    Notes
    -----
    The point of this function is to find the bestfit frame through the given points
    and transform the points to make the problem 2D.

    Once in 2D, the problem simplifies to finding the center point that minimises
    the difference between the resulting circles for all given points, i.e.
    minimise in the least squares sense the deviation between the individual
    radii and the average radius.

    For more information see [1]_.

    References
    ----------
    .. [1] Scipy. *Least squares circle*.
           Available at: http://scipy-cookbook.readthedocs.io/items/Least_Squares_Circle.html.

    Examples
    --------
    >>>

    """
    o, uvw, _ = pca_numpy(points)
    frame = [o, uvw[1], uvw[2]]

    rst = world_to_local_coordinates_numpy(frame, points)

    x = rst[:, 0]
    y = rst[:, 1]

    def dist(xc, yc):
        # compute the radius of the circle through each of the given points
        # for the current centre point
        return sqrt((x - xc) ** 2 + (y - yc) ** 2)

    def f(c):
        # compute the deviation of the radius of each sample point
        # from the average radius
        # => minimize this deviation
        Ri = dist(*c)
        return Ri - Ri.mean()

    xm = mean(x)
    ym = mean(y)
    c0 = xm, ym
    c, error = leastsq(f, c0)

    # compute the radius of the circle through each sample point for the
    # computed center point.
    Ri = dist(*c)

    # compute the radius of the bestfit circle as the average of the individual
    # radii.
    R = Ri.mean()

    # residu = sum((Ri - R) ** 2)
    # print(residu)

    # convert the location of the center point back to global coordinates.
    xyz = local_to_world_coordinates_numpy(frame, [[c[0], c[1], 0.0]])[0]
    return xyz, uvw[2], R


def bestfit_sphere_numpy(points):
    """Returns the sphere's center and radius that fits best through a set of points.

    Parameters
    ----------
    points: list of points
        XYZ coordinates of the points.

    Returns
    -------
    tuple: center, radius
        sphere center (XYZ coordinates) and sphere radius.

    Notes
    -----
    For more information see [1]_.

    References
    ----------
    .. [1] Least Squares Sphere Fit.
           Available at: https://jekel.me/2015/Least-Squares-Sphere-Fit/.

    Examples
    --------
    >>> from compas.geometry import bestfit_sphere_numpy
    >>> points = [(291.580, -199.041, 120.194), (293.003, -52.379, 33.599),\
                  (514.217, 26.345, 29.143), (683.253, 26.510, -6.194),\
                  (683.247, -327.154, 179.113), (231.606, -430.659, 115.458),\
                  (87.278, -419.178, -18.863), (24.731, -340.222, -127.158)]
    >>> center, radius = bestfit_sphere_numpy(points)
    """

    # Assemble the A matrix
    spX = asarray([p[0] for p in points])
    spY = asarray([p[1] for p in points])
    spZ = asarray([p[2] for p in points])
    A = zeros((len(spX), 4))
    A[:, 0] = spX*2
    A[:, 1] = spY*2
    A[:, 2] = spZ*2
    A[:, 3] = 1

    # Assemble the f matrix
    f = zeros((len(spX), 1))
    f[:, 0] = (spX*spX) + (spY*spY) + (spZ*spZ)
    C, residules, rank, singval = lstsq(A, f)

    # solve for the radius
    t = (C[0]*C[0]) + (C[1]*C[1]) + (C[2]*C[2]) + C[3]
    radius = sqrt(t)
    return [float(C[0][0]), float(C[1][0]), float(C[2][0])], radius


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    import doctest
    doctest.testmod(globs=globals())
