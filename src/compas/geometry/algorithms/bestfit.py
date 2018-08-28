from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas.geometry.basic import subtract_vectors
from compas.geometry.basic import normalize_vector
from compas.geometry.basic import cross_vectors

from compas.geometry.average import centroid_points


__all__ = [
    'bestfit_plane',
    'bestfit_plane_numpy',
    'bestfit_circle_numpy',
]


# ==============================================================================
# bestfit plane
# ==============================================================================


def bestfit_plane(points):
    """Fit a plane to a list of (more than three) points.

    Parameters
    ----------
    points : list of list
        A list of points represented by their XYZ coordinates.

    Returns
    -------
    plane : tuple
        Base point and normal vector (normalized).

    Notes
    -----
    This method will minimize the squares of the residuals as perpendicular
    to the main axis, not the residuals perpendicular to the plane. If the
    residuals are small (i.e. your points all lie close to the resulting plane),
    then this method will probably suffice. However, if your points are more
    spread then this method may not be the best fit. For more information see
    [ernerfeldt2015]_

    References
    ----------
    .. [ernerfeldt2015] Ernerfeldt, E. *Fitting a plane to many points in 3D*.
                        Available at: http://www.ilikebigbits.com/blog/2015/3/2/plane-from-points

    Examples
    --------
    .. code-block:: python

        #

    See also
    --------
    :func:`bestfit_plane_numpy` : Variation using NumPy.

    """
    centroid = centroid_points(points)

    xx, xy, xz = 0., 0., 0.
    yy, yz, zz = 0., 0., 0.

    for point in points:
        rx, ry, rz = subtract_vectors(point, centroid)
        xx += rx * rx
        xy += rx * ry
        xz += rx * rz
        yy += ry * ry
        yz += ry * rz
        zz += rz * rz

    det_x = yy * zz - yz * yz
    det_y = xx * zz - xz * xz
    det_z = xx * yy - xy * xy

    det_max = max(det_x, det_y, det_z)

    if det_max == det_x:
        a = (xz * yz - xy * zz) / det_x
        b = (xy * yz - xz * yy) / det_x
        normal = (1., a, b)
    elif det_max == det_y:
        a = (yz * xz - xy * zz) / det_y
        b = (xy * xz - yz * xx) / det_y
        normal = (a, 1., b)
    else:
        a = (yz * xy - xz * yy) / det_z
        b = (xz * xy - yz * xx) / det_z
        normal = (a, b, 1.)

    return centroid, normalize_vector(normal)


def bestfit_plane_numpy(points):
    """Fit a plane through more than three (non-coplanar) points.

    Warning
    -------
    This function requires Numpy and Scipy.

    Parameters
    ----------
    points : list
        XYZ coordinates of the points.

    Returns
    -------
    tuple
        A point on the plane, and the normal vector.

    See also
    --------
    :func:`bestfit_plane_numpy2`
    :func:`bestfit_plane_numpy3`
    :func:`bestfit_plane_numpy4`

    Examples
    --------
    .. code-block:: python

        #

    """
    from numpy import asarray
    from numpy import sum
    from scipy.linalg import svd

    xyz = asarray(points).reshape((-1, 3))
    n = xyz.shape[0]
    m = 1.0 / (n - 1.0)
    c = (sum(xyz, axis=0) / n).reshape((-1, 3))
    Yt = xyz - c
    C = m * Yt.T.dot(Yt)
    u, s, vT = svd(C)
    w = vT[2, :]
    return c, w


# @see: https://stackoverflow.com/questions/35070178/fit-plane-to-a-set-of-points-in-3d-scipy-optimize-minimize-vs-scipy-linalg-lsts
# @see: https://stackoverflow.com/questions/20699821/find-and-draw-regression-plane-to-a-set-of-points/20700063#20700063
# @see: http://www.ilikebigbits.com/blog/2015/3/2/plane-from-points
# @see: https://math.stackexchange.com/questions/99299/best-fitting-plane-given-a-set-of-points


def bestfit_plane_numpy2(points):
    from numpy import asarray
    from numpy import sum
    from numpy import hstack
    from numpy import ones
    from scipy.linalg import solve

    xyz = asarray(points).reshape((-1, 3))
    n = xyz.shape[0]
    c = (sum(xyz, axis=0) / n).reshape((-1, 3))
    A = hstack((xyz[:, 0:2], ones((xyz.shape[0], 1))))
    b = xyz[:, 2:]
    a, b, c = solve(A.T.dot(A), A.T.dot(b))
    u = 1.0, 0.0, a[0]
    v = 0.0, 1.0, b[0]
    w = normalize_vector(cross_vectors(u, v))
    return c, w


def bestfit_plane_numpy3(points):
    from numpy import asarray
    from numpy import sum
    from functools import partial
    from scipy.optimize import minimize

    def plane(x, y, abc):
        a, b, c = abc
        return a * x + b * y + c

    def error(abc, points):
        result = 0
        for x, y, z in points:
            znew = plane(x, y, abc)
            result += (znew - z) ** 2
        return result

    c = sum(asarray(points), axis=0) / len(points)
    objective = partial(error, points=points)
    res = minimize(objective, [0, 0, 0])
    a, b, c = res.x
    u = 1.0, 0.0, a
    v = 0.0, 1.0, b
    w = normalize_vector(cross_vectors(u, v))
    return c, w


def bestfit_plane_numpy4(points):
    from compas.numerical import pca_numpy

    c, (_, _, w), _ = pca_numpy(points)
    return c, w


# ==============================================================================
# bestfit circle
# ==============================================================================


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
    For more information see [1]_.

    References
    ----------
    .. [1] Scipy. *Least squares circle*.
           Available at: http://scipy-cookbook.readthedocs.io/items/Least_Squares_Circle.html.

    Examples
    --------
    .. code-block:: python

        #

    """
    from numpy import sqrt
    from numpy import mean
    from numpy import sum

    from scipy.optimize import leastsq

    from compas.numerical import pca_numpy
    from compas.geometry import local_coords_numpy
    from compas.geometry import global_coords_numpy

    o, uvw, _ = pca_numpy(points)
    rst = local_coords_numpy(o, uvw, points)
    x = rst[:, 0]
    y = rst[:, 1]

    def dist(xc, yc):
        return sqrt((x - xc) ** 2 + (y - yc) ** 2)

    def f(c):
        Ri = dist(*c)
        return Ri - Ri.mean()

    xm     = mean(x)
    ym     = mean(y)
    c0     = xm, ym
    c, ier = leastsq(f, c0)
    Ri     = dist(*c)
    R      = Ri.mean()
    residu = sum((Ri - R) ** 2)

    print(residu)

    xyz = global_coords_numpy(o, uvw, [[c[0], c[1], 0.0]])[0]

    o = xyz.tolist()
    u, v, w = uvw.tolist()

    return o, w, R


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    pass
