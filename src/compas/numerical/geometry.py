from __future__ import print_function

from functools import partial

from numpy import asarray
from numpy import array
from numpy import meshgrid
from numpy import linspace
from numpy import amax
from numpy import amin
from numpy import sum
from numpy import newaxis
from numpy import ones
from numpy import hstack
from numpy import sqrt
from numpy import mean

from scipy.linalg import svd
from scipy.linalg import solve
from scipy.optimize import minimize
from scipy.optimize import leastsq

from scipy.interpolate import griddata

import matplotlib.pyplot as plt

from compas.geometry import cross_vectors

from compas.numerical.linalg import normrow
from compas.numerical.statistics import principal_components as pca
from compas.numerical.spatial import _compute_local_coords
from compas.numerical.spatial import _compute_global_coords
from compas.numerical.operators import grad


__author__     = ['Tom Van Mele <vanmelet@ethz.ch>',
                  'Andrew Liew <liew@arch.ethz.ch>']
__copyright__  = 'Copyright 2016, Block Research Group - ETH Zurich'
__license__    = 'MIT License'
__email__      = 'liew@arch.ethz.ch'


__all__ = [
    'uvw_lengths',
    'scalarfield_contours',
    'plot_scalarfield_contours',
]


def uvw_lengths(C, X):
    r"""Calculates the lengths and co-ordinate differences.

    Parameters:
        C (sparse): Connectivity matrix (m x n)
        X (array): Co-ordinates of vertices/points (n x 3).

    Returns:
        array: Vectors of co-ordinate differences in x, y and z (m x 3).
        array: Lengths of members (m x 1)

    Examples:
        >>> C = connectivity_matrix([[0, 1], [1, 2]], 'csr')
        >>> X = array([[0, 0, 0], [1, 1, 0], [0, 0, 1]])
        >>> uvw
        array([[ 1,  1,  0],
               [-1, -1,  1]])
        >>> l
        array([[ 1.41421356],
               [ 1.73205081]])
    """
    uvw = C.dot(X)
    return uvw, normrow(uvw)


def trimesh_descent(trimesh):
    """"""
    vertices, faces = trimesh.to_vertices_and_faces()
    V = array(vertices)
    F = array(faces)
    G = grad(V, F)
    sfield = V[:, 2].reshape((-1, 1))
    vfield = - G.dot(sfield)
    return vfield.reshape((-1, 3), order='F').tolist()


# ==============================================================================
# contours
# ==============================================================================


def scalarfield_contours(xy, s, N=50):
    r"""Compute the contour lines of a scalarfield.

    The computation of the contour lines is based on the ``contours`` function
    available through matplotlib
    (`<http://matplotlib.org/api/_as_gen/matplotlib.axes.Axes.contour.html#matplotlib.axes.Axes.contour>`_).

    Parameters:
        xy (array-like): The xy-coordinates at which the scalar field is defined.
        s (array-like): The values of the scalar field.
        N (int): Optional. The number of contour lines to compute. Default is ``50``.

    Returns:
        tuple: A tuple of a list of levels and a list of contour geometry.

        The list of levels contains the values of the scalarfield at each of
        the contours. The second item in the tuple is a list of contour lines.
        Each contour line is a list of paths, and each path is a list polygons.

    Examples:

        .. code-block:: python

            import compas
            from compas.datastructures.mesh import Mesh
            from compas.geometry import centroid_points
            from compas.geometry import distance_point_point

            mesh = Mesh.from_obj(compas.get_data('faces.obj'))

            points = [mesh.vertex_coordinates(key) for key in mesh]
            centroid = centroid_points(points)

            distances = [distance_point_point(point, centroid) for point in points]

            xy = [[points[i][0], points[i][1]] for i in range(len(points))]

            levels, contours = contours_scalarfield(xy, distances)

            for i in range(len(contours)):
                level = levels[i]
                contour = contours[i]
                print(level)
                for path in contour:
                    for polygon in path:
                        print(polygon)


    See Also:

        :func:`compas.datastructures.numerical.geometry.mesh_contours`

    """
    xy = asarray(xy)
    s = asarray(s)
    x = xy[:, 0]
    y = xy[:, 1]
    X, Y = meshgrid(
        linspace(amin(x), amax(x), 2 * N),
        linspace(amin(y), amax(y), 2 * N)
    )
    S = griddata((x, y), s, (X, Y), method='cubic')
    ax = plt.figure().add_subplot(111, aspect='equal')
    c = ax.contour(X, Y, S, N)
    plt.draw()
    contours = [0] * len(c.collections)
    levels = c.levels
    for i, coll in enumerate(iter(c.collections)):
        paths = coll.get_paths()
        contours[i] = [0] * len(paths)
        for j, path in enumerate(iter(paths)):
            polygons = path.to_polygons()
            contours[i][j] = [0] * len(polygons)
            for k, polygon in enumerate(iter(polygons)):
                contours[i][j][k] = polygon.tolist()
    return levels, contours


def plot_scalarfield_contours(xy, s, N=50):
    r"""Plot the contours of a scalarfield.

    Parameters:
        xy (array-like): The xy-coordinates at which the scalar field is defined.
        s (array-like): The values of the scalar field.
        N (int): Optional. The number of contour lines to compute. Default is ``30``.

    Examples:

        .. code-block:: python

            import compas

            from compas.datastructures.mesh import Mesh
            from compas.geometry import centroid_points
            from compas.geometry import distance_point_point

            mesh = Mesh.from_obj(compas.get_data('faces.obj'))

            points = [mesh.vertex_coordinates(key) for key in mesh]
            centroid = centroid_points(points)

            xy = [[points[i][0], points[i][1]] for i in range(len(points))]
            d = [distance_point_point(point, centroid) for point in points]

            plot_scalarfield_contours(xy, d)


        .. plot::

            import compas
            from compas.datastructures.mesh import Mesh
            from compas.geometry import centroid_points
            from compas.geometry import distance_point_point
            from compas.numerical.geometry import plot_scalarfield_contours

            mesh = Mesh.from_obj(compas.get_data('faces.obj'))
            points = [mesh.vertex_coordinates(key) for key in mesh]
            centroid = centroid_points(points)
            d = [distance_point_point(point, centroid) for point in points]
            xy = [[points[i][0], points[i][1]] for i in range(len(points))]

            plot_scalarfield_contours(xy, d)

    See Also:

        :func:`compas.datastructures.mesh.numerical.geometry.plot_mesh_contours`

    """
    xy = asarray(xy)
    s = asarray(s)
    x = xy[:, 0]
    y = xy[:, 1]
    X, Y = meshgrid(
        linspace(amin(x), amax(x), 2 * N),
        linspace(amin(y), amax(y), 2 * N)
    )
    S = griddata((x, y), s, (X, Y), method='cubic')
    ax = plt.figure().add_subplot(111, aspect='equal')
    ax.contour(X, Y, S, N)
    plt.show()


def mesh_contours(mesh, N=50):
    """Compute the contours of the mesh.

    The contours are defined as the isolines of the z-coordinates of the vertices
    of the mesh.

    Parameters:
        mesh (:class:`compas.datastructures.mesh.Mesh`): The mesh object.
        N (int): Optional. The density of the contours. Default is ``50``.

    Returns:
        tuple: A tuple of a list of levels and a list of contours.

        The list of levels contains the z-values at each of the contours.
        Each contour is a list of paths, and each path is a list polygons.

    Examples:

        .. code-block:: python

            import compas
            from compas.datastructures.mesh import Mesh

            mesh = Mesh.from_obj(compas.get_data('hypar.obj'))
            print(mesh_contours(mesh))

    See Also:
        :func:`compas.numerical.geometry.scalarfield_contours`

    """
    xy = [mesh.vertex_coordinates(key, 'xy') for key in mesh.vertices()]
    z = [mesh.vertex_coordinates(key, 'z') for key in mesh.vertices()]
    return scalarfield_contours(xy, z, N)


def mesh_isolines(mesh, attr_name, N=50):
    """Compute the isolines of a specified attribute of the vertices of a mesh.

    Parameters:
        mesh (:class:`compas.datastructures.mesh.Mesh`): A mesh object.
        attr_name (str): The name of the vertex attribute.
        N (int): Optional. The density of the isolines. Default is ``50``.

    Returns:
        tuple: A tuple of a list of levels and a list of isolines.

        The list of levels contains the z-values at each of the isolines.
        Each isoline is a list of paths, and each path is a list polygons.

    See Also:
        :func:`compas.numerical.geometry.scalarfield_contours`

    """
    xy = [mesh.vertex_coordinates(key, 'xy') for key in mesh.vertices()]
    s = [mesh.vertex[key][attr_name] for key in mesh.vertices()]
    return scalarfield_contours(xy, s, N)


def plot_mesh_contours(mesh, N=50):
    """Plot the contours of a mesh.

    Parameters:
        mesh (:class:`compas.datastructures.mesh.Mesh`): The mesh object.
        N (int): The density of the plot.

    Examples:

        .. code-block:: python

            import compas
            from compas.datastructures.mesh import Mesh
            from compas.datastructures.mesh.numerical import plot_mesh_contours

            mesh = Mesh.from_obj(compas.get_data('hypar.obj'))

            plot_mesh_contours(mesh, N=50)


        .. plot::

            import compas
            from compas.datastructures.mesh import Mesh
            from compas.datastructures.mesh.numerical import plot_mesh_contours
            mesh = Mesh.from_obj(compas.get_data('hypar.obj'))
            plot_mesh_contours(mesh, N=50)


    See Also:
        :func:`compas.numerical.geometry.plot_scalarfield_contours`

    """
    xy = [mesh.vertex_coordinates(key, 'xy') for key in mesh.vertices()]
    z = [mesh.vertex_coordinates(key, 'z')[0] for key in mesh.vertices()]
    plot_scalarfield_contours(xy, z, N)


def plot_mesh_isolines(mesh, attr_name, N=50):
    """Plot the isolines of a vertex attribute of the mesh.

    Parameters:
        mesh (:class:`compas.datastructures.mesh.Mesh`): A mesh object.
        attr_name (str): The name of the vertex attribute.
        N (int): Optional. The density of the isolines. Default is ``50``.

    Examples:

        .. code-block:: python

            import compas
            from compas.datastructures.mesh import Mesh
            from compas.geometry import centroid_points
            from compas.geometry import distance_point_point
            from compas.datastructures.mesh.numerical import plot_mesh_isolines

            mesh = Mesh.from_obj(compas.get_data('faces.obj'))
            points = [mesh.vertex_coordinates(key) for key in mesh]
            centroid = centroid_points(points)

            for key, attr in mesh.vertices_iter(True):
                xyz = mesh.vertex_coordinates(key)
    `            attr['d'] = distance_point_point(xyz, centroid)

            plot_mesh_isolines(mesh, 'd')


        .. plot::

            import compas
            from compas.datastructures.mesh import Mesh
            from compas.geometry import centroid_points
            from compas.geometry import distance_point_point
            from compas.datastructures.mesh.numerical import plot_mesh_isolines
            mesh = Mesh.from_obj(compas.get_data('faces.obj'))
            points = [mesh.vertex_coordinates(key) for key in mesh]
            centroid = centroid_points(points)
            for key, attr in mesh.vertices_iter(True):
                xyz = mesh.vertex_coordinates(key)
                attr['d'] = distance_point_point(xyz, centroid)
            plot_mesh_isolines(mesh, 'd')


    See Also:
        :func:`compas.numerical.geometry.plot_scalarfield_contours`

    """
    xy = [mesh.vertex_coordinates(key, 'xy') for key in mesh.vertices()]
    s = [mesh.vertex[key][attr_name] for key in mesh.vertices()]
    plot_scalarfield_contours(xy, s, N)


# ==============================================================================
# bestfit plane
# ==============================================================================


# @see: https://stackoverflow.com/questions/35070178/fit-plane-to-a-set-of-points-in-3d-scipy-optimize-minimize-vs-scipy-linalg-lsts
# @see: https://stackoverflow.com/questions/20699821/find-and-draw-regression-plane-to-a-set-of-points/20700063#20700063
# @see: http://www.ilikebigbits.com/blog/2015/3/2/plane-from-points
# @see: https://math.stackexchange.com/questions/99299/best-fitting-plane-given-a-set-of-points


def bestfit_plane(points):
    xyz = asarray(points).reshape((-1, 3))
    n = xyz.shape[0]
    m = 1.0 / (n - 1.0)
    c = (sum(xyz, axis=0) / n).reshape((-1, 3))
    Yt = xyz - c
    C = m * Yt.T.dot(Yt)
    u, s, vT = svd(C)
    w = vT[2, :]
    return c, w


def bestfit_plane2(points):
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


def bestfit_plane3(points):
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


def bestfit_plane4(points):
    c, (_, _, w), _ = pca(points)
    return c, w


def bestfit_plane5(points):
    pass


# http://scipy-cookbook.readthedocs.io/items/Least_Squares_Circle.html

def bestfit_circle(points):
    o, uvw, _ = pca(points)
    rst = _compute_local_coords(o, uvw, points)
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

    xyz = _compute_global_coords(o, uvw, [[c[0], c[1], 0.0]])[0]
    return xyz.tolist(), uvw.tolist(), R


# ==============================================================================
# intersections
# ==============================================================================


def betfit_intersection(lines):
    l1 = np.array([[-2, 0], [0, 1]], dtype=float).T
    l2 = np.array([[0, -2], [1, 0]], dtype=float).T
    l3 = np.array([[5, 0], [0, 7]], dtype=float).T
    l4 = np.array([[3, 0], [0, 20]], dtype=float).T

    p1 = l1[:, 0].reshape((-1, 1))
    p2 = l2[:, 0].reshape((-1, 1))
    p3 = l3[:, 0].reshape((-1, 1))
    p4 = l4[:, 0].reshape((-1, 1))

    n1 = (l1[:, 1] - l1[:, 0]).reshape((-1, 1))
    n2 = (l2[:, 1] - l2[:, 0]).reshape((-1, 1))
    n3 = (l3[:, 1] - l3[:, 0]).reshape((-1, 1))
    n4 = (l4[:, 1] - l4[:, 0]).reshape((-1, 1))

    n1 = n1 / np.linalg.norm(n1)
    n2 = n2 / np.linalg.norm(n2)
    n3 = n3 / np.linalg.norm(n3)
    n4 = n4 / np.linalg.norm(n4)

    # an eye matrix (ones on the diagonal)

    I = np.eye(2, dtype=float)

    # R.p = q

    R = (I - n1.dot(n1.T)) + (I - n2.dot(n2.T)) + (I - n3.dot(n3.T)) + (I - n4.dot(n4.T))
    q = (I - n1.dot(n1.T)).dot(p1) + (I - n2.dot(n2.T)).dot(p2) + (I - n3.dot(n3.T)).dot(p3) + (I - n4.dot(n4.T)).dot(p4)

    RtR = R.T.dot(R)
    Rtq = R.T.dot(q)

    p = np.linalg.solve(RtR, Rtq)

    # plot the lines

    xy1 = p1 + n1 * np.arange(10)
    xy2 = p2 + n2 * np.arange(10)
    xy3 = p3 + n3 * np.arange(10)
    xy4 = p4 + n4 * np.arange(10)


# ==============================================================================
# Debugging
# ==============================================================================

if __name__ == "__main__":

    from mpl_toolkits.mplot3d import Axes3D

    import compas

    from compas.datastructures.mesh import Mesh
    from compas.geometry import normalize_vector

    mesh = Mesh.from_obj(compas.get_data('hypar.obj'))

    # points = [mesh.vertex_coordinates(key) for key in mesh]
    # centroid = centroid_points(points)

    # distances = [distance_point_point(point, centroid) for point in points]

    # xy = [[points[i][0], points[i][1]] for i in range(len(points))]

    # plot_scalarfield_contours(xy, distances, 20)

    fkey = mesh.get_any_face()

    points = mesh.face_coordinates(fkey)

    n0 = normalize_vector(mesh.face_normal(fkey))

    c, uvw, R = bestfit_circle(points)

    _, n1 = bestfit_plane(points)
    _, n2 = bestfit_plane2(points)
    _, n3 = bestfit_plane3(points)
    _, n4 = bestfit_plane4(points)

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
