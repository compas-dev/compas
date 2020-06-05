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

from compas.numerical import scalarfield_contours_numpy


__all__ = [
    'mesh_isolines_numpy',
    'mesh_contours_numpy',
]


def mesh_isolines_numpy(mesh, attr_name, N=50):
    """Compute the isolines of a specified attribute of the vertices of a mesh.

    Parameters
    ----------
    mesh : Mesh
        A mesh object.
    attr_name : str
        The name of the vertex attribute.
    N : int (50)
        The density of the isolines.
        Default is ``50``.

    Returns
    -------
    tuple
        A tuple of a list of levels and a list of isolines.

        The list of levels contains the z-values at each of the isolines.
        Each isoline is a list of paths, and each path is a list polygons.

    """
    xy = [mesh.vertex_coordinates(key, 'xy') for key in mesh.vertices()]
    s = [mesh.vertex[key][attr_name] for key in mesh.vertices()]
    return scalarfield_contours_numpy(xy, s, N)


def mesh_contours_numpy(mesh, levels=None, density=100):
    """Compute the contours of the mesh.

    Parameters
    ----------
    mesh : Mesh
        The mesh object.
    N : int, optional
        The density of the contours.
        Default is ``50``.

    Returns
    -------
    tuple
        A tuple of a list of levels and a list of contours.

        The list of levels contains the z-values at each of the contours.
        Each contour is a list of paths, and each path is a list polygons.

    Notes
    -----
    The contours are defined as the isolines of the z-coordinates of the vertices
    of the mesh.

    """
    xy = [mesh.vertex_attributes(key, 'xy') for key in mesh.vertices()]
    z = [mesh.vertex_attribute(key, 'z') for key in mesh.vertices()]

    xy = asarray(xy)
    z = asarray(z)
    x = xy[:, 0]
    y = xy[:, 1]

    if not levels:
        levels = 50

    X, Y = meshgrid(linspace(amin(x), amax(x), 2 * density),
                    linspace(amin(y), amax(y), 2 * density))

    Z = griddata((x, y), z, (X, Y), method='cubic')

    fig = plt.figure()
    ax = fig.add_subplot(111, aspect='equal')
    c = ax.contour(X, Y, Z, levels)

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

    import doctest
    doctest.testmod(globs=globals())
