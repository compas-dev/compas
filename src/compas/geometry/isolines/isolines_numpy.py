from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from numpy import asarray
from numpy import meshgrid
from numpy import linspace
from numpy import amax
from numpy import amin
from scipy.interpolate import griddata
import matplotlib.pyplot as plt


__all__ = [
    'scalarfield_contours_numpy',
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


def scalarfield_contours_numpy(xy, s, levels=50, density=100):
    r"""Compute the contour lines of a scalarfield.

    Parameters
    ----------
    xy : array-like
        The xy-coordinates at which the scalar field is defined.
    s : array-like
        The values of the scalar field.
    levels : int, optional
        The number of contour lines to compute.
        Default is ``50``.

    Returns
    -------
    tuple
        A tuple of a list of levels and a list of contour geometry.

        The list of levels contains the values of the scalarfield at each of
        the contours. The second item in the tuple is a list of contour lines.
        Each contour line is a list of paths, and each path is a list polygons.

    Notes
    -----
    The computation of the contour lines is based on the `contours function`_
    available through matplotlib.

    Examples
    --------
    .. code-block:: python

        import compas
        from compas.datastructures import Mesh
        from compas.geometry import centroid_points
        from compas.geometry import distance_point_point
        from compas.geometry import scalarfield_contours_numpy

        mesh = Mesh.from_obj(compas.get('faces.obj'))

        points = [mesh.vertex_coordinates(key) for key in mesh.vertices()]
        centroid = centroid_points(points)
        distances = [distance_point_point(point, centroid) for point in points]

        xy = [point[0:2] for point in points]

        levels, contours = scalarfield_contours_numpy(xy, distances)

        for i in range(len(contours)):
            level = levels[i]
            contour = contours[i]
            print(level)
            for path in contour:
                for polygon in path:
                    print(polygon)

    .. _contours function: http://matplotlib.org/api/_as_gen/matplotlib.axes.Axes.contour.html#matplotlib.axes.Axes.contour

    """
    xy = asarray(xy)
    s = asarray(s)
    x = xy[:, 0]
    y = xy[:, 1]
    X, Y = meshgrid(linspace(amin(x), amax(x), 2 * density),
                    linspace(amin(y), amax(y), 2 * density))
    S = griddata((x, y), s, (X, Y), method='cubic')

    fig = plt.figure()
    ax = fig.add_subplot(111, aspect='equal')

    c = ax.contour(X, Y, S, levels)

    contours = [0] * len(c.collections)
    levels = c.levels

    for i, coll in enumerate(iter(c.collections)):
        paths = coll.get_paths()
        contours[i] = [0] * len(paths)
        for j, path in enumerate(iter(paths)):
            polygons = path.to_polygons()
            contours[i][j] = [0] * len(polygons)
            for k, polygon in enumerate(iter(polygons)):
                contours[i][j][k] = polygon

    plt.close(fig)

    return levels, contours


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    import compas
    from compas.datastructures import Mesh
    from compas.geometry import centroid_points
    from compas.geometry import distance_point_point

    mesh = Mesh.from_obj(compas.get('faces.obj'))

    points = [mesh.vertex_coordinates(key) for key in mesh.vertices()]
    centroid = centroid_points(points)
    distances = [distance_point_point(point, centroid) for point in points]

    xy = [point[0:2] for point in points]

    levels, contours = scalarfield_contours_numpy(xy, distances)

    # xy = [mesh.vertex_attributes(key, 'xy') for key in mesh.vertices()]
    # z = [mesh.vertex_attribute(key, 'z') for key in mesh.vertices()]
    # levels, contours = scalarfield_contours_numpy(xy, z)

    # levels, contours = mesh_contours_numpy(mesh)

    for i in range(len(contours)):
        level = levels[i]
        contour = contours[i]
        print(level)
        for path in contour:
            for polygon in path:
                print([point.tolist() for point in polygon])
