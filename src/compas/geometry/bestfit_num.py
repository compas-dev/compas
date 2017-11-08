from __future__ import print_function
from __future__ import division

from functools import partial

from compas.geometry.basic import normalize_vector
from compas.geometry.basic import cross_vectors

from numpy import array
from numpy import arange
from numpy import asarray
from numpy import sum
from numpy import eye
from numpy import sqrt
from numpy import mean
from numpy import hstack
from numpy import ones

from scipy.optimize import minimize
from scipy.optimize import leastsq
from scipy.linalg import norm
from scipy.linalg import solve
from scipy.linalg import svd

from compas.numerical import principal_component_analysis as pca
from compas.numerical import compute_local_coords
from compas.numerical import compute_global_coords


__author__     = ['Tom Van Mele <vanmelet@ethz.ch>',
                  'Matthias Rippmann <rippmann@ethz.ch>']
__copyright__  = 'Copyright 2014, Block Research Group - ETH Zurich'
__license__    = 'MIT License'
__email__      = '<vanmelet@ethz.ch>'


__all__ = [
    'bestfit_plane_numpy',
    'bestfit_circle_numpy',
    'bestfit_intersection_numpy'
]


# ==============================================================================
# bestfit plane
# ==============================================================================


def bestfit_plane_numpy(points):
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
    c, (_, _, w), _ = pca(points)
    return c, w


# ==============================================================================
# bestfit circle
# ==============================================================================


# http://scipy-cookbook.readthedocs.io/items/Least_Squares_Circle.html
def bestfit_circle_numpy(points):
    o, uvw, _ = pca(points)
    rst = compute_local_coords(o, uvw, points)
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
    residu = sum((Ri - R)**2)

    print(residu)

    xyz = compute_global_coords(o, uvw, [[c[0], c[1], 0.0]])[0]
    return xyz.tolist(), uvw.tolist(), R


# ==============================================================================
# bestfit intersection
# ==============================================================================


def bestfit_intersection_numpy(lines):
    l1 = array([[-2, 0], [0, 1]], dtype=float).T
    l2 = array([[0, -2], [1, 0]], dtype=float).T
    l3 = array([[5, 0], [0, 7]], dtype=float).T
    l4 = array([[3, 0], [0, 20]], dtype=float).T

    p1 = l1[:, 0].reshape((-1, 1))
    p2 = l2[:, 0].reshape((-1, 1))
    p3 = l3[:, 0].reshape((-1, 1))
    p4 = l4[:, 0].reshape((-1, 1))

    n1 = (l1[:, 1] - l1[:, 0]).reshape((-1, 1))
    n2 = (l2[:, 1] - l2[:, 0]).reshape((-1, 1))
    n3 = (l3[:, 1] - l3[:, 0]).reshape((-1, 1))
    n4 = (l4[:, 1] - l4[:, 0]).reshape((-1, 1))

    n1 = n1 / norm(n1)
    n2 = n2 / norm(n2)
    n3 = n3 / norm(n3)
    n4 = n4 / norm(n4)

    # an eye matrix (ones on the diagonal)

    I = eye(2, dtype=float)

    # R.p = q

    R = (I - n1.dot(n1.T)) + (I - n2.dot(n2.T)) + (I - n3.dot(n3.T)) + (I - n4.dot(n4.T))
    q = (I - n1.dot(n1.T)).dot(p1) + (I - n2.dot(n2.T)).dot(p2) + (I - n3.dot(n3.T)).dot(p3) + (I - n4.dot(n4.T)).dot(p4)

    RtR = R.T.dot(R)
    Rtq = R.T.dot(q)

    p = solve(RtR, Rtq)

    # plot the lines

    xy1 = p1 + n1 * arange(10)
    xy2 = p2 + n2 * arange(10)
    xy3 = p3 + n3 * arange(10)
    xy4 = p4 + n4 * arange(10)


# ==============================================================================
# Debugging
# ==============================================================================

if __name__ == "__main__":

    import matplotlib.pyplot as plt
    from mpl_toolkits.mplot3d import Axes3D

    import compas

    from compas.datastructures.mesh import Mesh

    mesh = Mesh.from_obj(compas.get_data('hypar.obj'))

    fkey = mesh.get_any_face()

    points = mesh.face_coordinates(fkey)

    n0 = normalize_vector(mesh.face_normal(fkey))

    c, uvw, R = bestfit_circle_numpy(points)

    _, n1 = bestfit_plane_numpy(points)
    _, n2 = bestfit_plane_numpy2(points)
    _, n3 = bestfit_plane_numpy3(points)
    _, n4 = bestfit_plane_numpy4(points)

    print(n0)
    print(n1)
    print(n2)
    print(n3)
    print(n4)

    x, y, z = zip(*points)

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    ax.scatter(x, y, z)
    ax.plot([c[0]], [c[1]], [c[2]], 'ro')

    ax.set_xlim(-1, 1)
    ax.set_ylim(-1, 1)
    ax.set_zlim(2, 3)

    plt.show()

