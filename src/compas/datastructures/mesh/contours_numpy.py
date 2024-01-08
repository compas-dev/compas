from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas.numerical import scalarfield_contours


def mesh_isolines_numpy(mesh, attr_name, N=50):
    """Compute the isolines of a specified attribute of the vertices of a mesh.

    Parameters
    ----------
    mesh : :class:`compas.datastructures.Mesh`
        A mesh object.
    attr_name : str
        The name of the vertex attribute.
    N : int, optional
        The density of the isolines.

    Returns
    -------
    list[float]
        A list of levels.
    list[list[float]]
        A list of isolines.
        The list of levels contains the z-values at each of the isolines.
        Each isoline is a list of paths, and each path is a list polygons.

    """
    xy = mesh.vertices_attributes("xy")
    s = mesh.vertices_attribute(attr_name)
    return scalarfield_contours(xy, s, N)


def mesh_contours_numpy(mesh, levels=50):
    """Compute the contours of the mesh.

    Parameters
    ----------
    mesh : :class:`compas.datastructures.Mesh`
        The mesh object.
    levels : int, optional
        The number of contours.

    Returns
    -------
    list[float]
        A list of levels.
    list[list[float]]
        A list of contours.
        The list of levels contains the z-values at each of the contours.
        Each contour is a list of paths, and each path is a list polygons.

    Notes
    -----
    The contours are defined as the isolines of the z-coordinates of the vertices of the mesh.

    """
    xy = mesh.vertices_attributes("xy")
    z = mesh.vertices_attribute("z")
    return scalarfield_contours(xy, z, levels)
