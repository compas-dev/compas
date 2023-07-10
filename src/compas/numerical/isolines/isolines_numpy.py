from numpy import asarray
from numpy import meshgrid
from numpy import linspace
from numpy import amax
from numpy import amin
from scipy.interpolate import griddata  # type: ignore
import matplotlib.pyplot as plt


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
    X, Y = meshgrid(linspace(amin(x), amax(x), 2 * density), linspace(amin(y), amax(y), 2 * density))
    S = griddata((x, y), s, (X, Y), method="cubic")

    fig = plt.figure()
    ax = fig.add_subplot(111, aspect="equal")

    c = ax.contour(X, Y, S, levels)

    contours = [0] * len(c.collections)  # type: ignore
    levels = c.levels  # type: ignore

    for i, coll in enumerate(iter(c.collections)):  # type: ignore
        paths = coll.get_paths()
        contours[i] = [0] * len(paths)  # type: ignore
        for j, path in enumerate(iter(paths)):
            polygons = path.to_polygons()
            contours[i][j] = [0] * len(polygons)  # type: ignore
            for k, polygon in enumerate(iter(polygons)):
                contours[i][j][k] = polygon  # type: ignore

    plt.close(fig)

    return levels, contours
