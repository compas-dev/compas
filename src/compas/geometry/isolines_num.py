from __future__ import print_function

from numpy import asarray
from numpy import meshgrid
from numpy import linspace
from numpy import amax
from numpy import amin

from scipy.interpolate import griddata

import matplotlib.pyplot as plt


__author__     = ['Tom Van Mele <vanmelet@ethz.ch>',
                  'Andrew Liew <liew@arch.ethz.ch>']
__copyright__  = 'Copyright 2016, Block Research Group - ETH Zurich'
__license__    = 'MIT License'
__email__      = 'liew@arch.ethz.ch'


__all__ = [
    'scalarfield_contours',
    'plot_scalarfield_contours',
    'mesh_contours',
    'mesh_isolines',
    'plot_mesh_contours',
    'plot_mesh_isolines'
]


# def trimesh_descent(trimesh):
#     """"""
#     vertices, faces = trimesh.to_vertices_and_faces()
#     V = array(vertices)
#     F = array(faces)
#     G = grad(V, F)
#     sfield = V[:, 2].reshape((-1, 1))
#     vfield = - G.dot(sfield)
#     return vfield.reshape((-1, 3), order='F').tolist()


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
            from compas.datastructures import Mesh
            from compas.geometry import centroid_points
            from compas.geometry import distance_point_point
            from compas.numerical import scalarfield_contours

            mesh = Mesh.from_obj(compas.get_data('faces.obj'))

            points = [mesh.vertex_coordinates(key) for key in mesh.vertices()]
            centroid = centroid_points(points)

            distances = [distance_point_point(point, centroid) for point in points]

            xy = [[points[i][0], points[i][1]] for i in range(len(points))]

            levels, contours = scalarfield_contours(xy, distances)

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

            from compas.datastructures import Mesh
            from compas.geometry import centroid_points
            from compas.geometry import distance_point_point
            from compas.numerical import plot_scalarfield_contours

            mesh = Mesh.from_obj(compas.get_data('faces.obj'))

            points = [mesh.vertex_coordinates(key) for key in mesh.vertices()]
            centroid = centroid_points(points)

            xy = [[points[i][0], points[i][1]] for i in range(len(points))]
            d = [distance_point_point(point, centroid) for point in points]

            plot_scalarfield_contours(xy, d)


        .. plot::

            import compas
            from compas.datastructures import Mesh
            from compas.geometry import centroid_points
            from compas.geometry import distance_point_point
            from compas.numerical import plot_scalarfield_contours

            mesh = Mesh.from_obj(compas.get_data('faces.obj'))
            points = [mesh.vertex_coordinates(key) for key in mesh.vertices()]
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
            from compas.datastructures import Mesh
            from compas.numerical import mesh_contours

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
        mesh (:class:`compas.datastructures.Mesh`): The mesh object.
        N (int): The density of the plot.

    Examples:

        .. plot::
            :include-source:

            import compas
            from compas.datastructures import Mesh
            from compas.numerical import plot_mesh_contours

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
        mesh (:class:`compas.datastructures.Mesh`): A mesh object.
        attr_name (str): The name of the vertex attribute.
        N (int): Optional. The density of the isolines. Default is ``50``.

    Examples:

        .. code-block:: python

            import compas
            from compas.datastructures import Mesh
            from compas.geometry import centroid_points
            from compas.geometry import distance_point_point
            from compas.numerical import plot_mesh_isolines

            mesh = Mesh.from_obj(compas.get_data('faces.obj'))
            points = [mesh.vertex_coordinates(key) for key in mesh.vertices()]
            centroid = centroid_points(points)

            for key, attr in mesh.vertices_iter(True):
                xyz = mesh.vertex_coordinates(key)
    `            attr['d'] = distance_point_point(xyz, centroid)

            plot_mesh_isolines(mesh, 'd')


        .. plot::

            import compas
            from compas.datastructures import Mesh
            from compas.geometry import centroid_points
            from compas.geometry import distance_point_point
            from compas.numerical import plot_mesh_isolines
            mesh = Mesh.from_obj(compas.get_data('faces.obj'))
            points = [mesh.vertex_coordinates(key) for key in mesh.vertices()]
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
# Debugging
# ==============================================================================

if __name__ == "__main__":

    pass
