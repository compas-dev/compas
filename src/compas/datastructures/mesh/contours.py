from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas

try:
    from numpy import asarray
    from numpy import meshgrid
    from numpy import linspace
    from numpy import amax
    from numpy import amin

    from scipy.interpolate import griddata

    import matplotlib.pyplot as plt

except ImportError:
    compas.raise_if_not_ironpython()

try:
    import pymesh
except ImportError:
    pass

from compas.geometry import scalarfield_contours_numpy


__all__ = [
    'mesh_isolines_numpy',
    'mesh_contours_numpy',
    'mesh_contours_pymesh'
]


def mesh_isolines_numpy(mesh, attr_name, N=50):
    """Compute the isolines of a specified attribute of the vertices of a mesh.

    Parameters
    ----------
    mesh : Mesh
        A mesh object.
    attr_name : str
        The name of the vertex attribute.
    N : int, optional
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

    Notes
    -----
    The contours are defined as the isolines of the z-coordinates of the vertices
    of the mesh.

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

    Examples
    --------
    .. code-block:: python

        import compas
        from compas.datastructures import Mesh
        from compas.geometry import mesh_contours_numpy

        mesh = Mesh.from_obj(compas.get('hypar.obj'))
        print(mesh_contours_numpy(mesh))

    """
    xy = [mesh.vertex_coordinates(key, 'xy') for key in mesh.vertices()]
    z = [mesh.get_vertex_attribute(key, 'z') for key in mesh.vertices()]

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


# def mesh_contours_skimage(mesh, levels=None, density=100):
#     pass


# def mesh_contours_opencv(mesh, levels=None, density=100):
#     pass


# def mesh_contours_vtk(mesh, levels=None, density=100):
#     pass


def mesh_contours_pymesh(mesh, levels=None, density=100):
    vertices, faces = mesh.to_vertices_and_faces()
    m = pymesh.form_mesh(vertices, faces)
    return pymesh.slice_mesh(m, [0, 0, 1], 50)


# def mesh_contours_igl(mesh, levels=None, density=100):
#     pass


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    import compas
    from compas.datastructures import Mesh
    from compas.datastructures import mesh_contours_numpy

    mesh = Mesh.from_obj(compas.get('saddle.obj'))

    # res = mesh_contours_pymesh(mesh)
    # print(res)

    levels, contours = mesh_contours_numpy(mesh)

    for i in range(len(contours)):
        level = levels[i]
        contour = contours[i]
        print(level)
        for path in contour:
            for polygon in path:
                print([point.tolist() for point in polygon])
