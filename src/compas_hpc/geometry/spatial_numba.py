
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from numba import f8
from numba import jit

from numpy import array
from numpy import min
from numpy import sqrt
from numpy import zeros


__all__ = [
    'distance_matrix_numba',
    'closest_distance_field_numba',
]


@jit(f8[:, :](f8[:, :], f8[:, :]), nogil=True, nopython=True, parallel=False, cache=True)
def distance_matrix_numba(A, B):

    """ Distance matrix between two point clouds.

    Parameters
    ----------
    A : array
        Point cloud 1 (m x 3).
    B : array
        Point cloud 2 (n x 3).

    Returns
    -------
    array
        Distance matrix (m x n).

    """

    m = A.shape[0]
    n = B.shape[0]
    o = zeros((m, n))

    for i in range(m):

        u = A[i, :]

        for j in range(n):

            v = B[j, :]

            dx = u[0] - v[0]
            dy = u[1] - v[1]
            dz = u[2] - v[2]

            o[i, j] = sqrt(dx**2 + dy**2 + dz**2)

    return o


def closest_distance_field_numba(x, y, z, points):

    """ Closest distance field between a grid and set of target points.

    Parameters
    ----------
    x : array
        Grid of x coordinates (m x n x o).
    y : array
        Grid of y coordinates (m x n x o).
    z : array
        Grid of z coordinates (m x n x o).
    points : array
        Target points to compare to (p x 3).

    Returns
    -------
    array
        Distance field array (m x n x o).

    """

    m, n, o   = x.shape
    distances = zeros((m, n, o))

    for i in range(m):
        for j in range(n):
            for k in range(o):

                point = array([[x[i, j, k], y[i, j, k], z[i, j, k]]])
                distances[i, j, k] = min(distance_matrix_numba(point, points))

    return distances


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    from numpy import hstack
    from numpy import linspace
    from numpy import meshgrid
    from numpy import newaxis

    from compas.viewers import VtkViewer


    # Grid

    n = 50
    a = linspace(-1, 1, n)
    xm, ym, zm = meshgrid(a, a, a)

    # Test points

    x = xm.ravel()
    y = ym.ravel()
    z = zm.ravel()

    r  = x**2 + y**2 + z**2
    lg = r < 0.05
    xs = x[lg][:, newaxis]
    ys = y[lg][:, newaxis]
    zs = z[lg][:, newaxis]

    points = hstack([xs, ys, zs])
    print(points.shape)

    # Distances

    distances = closest_distance_field_numba(xm, ym, zm, points)

    # View

    data   = {'voxels': distances}
    viewer = VtkViewer(data=data)
    viewer.setup()
    viewer.start()
