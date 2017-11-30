from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

try:
    from numpy import asarray
    from scipy.spatial import ConvexHull
except ImportError:
    import sys
    if 'ironpython' not in sys.version.lower():
        raise


__author__     = ['Matthias Rippmann <rippmann@ethz.ch>']
__copyright__  = 'Copyright 2014, Block Research Group - ETH Zurich'
__license__    = 'MIT License'
__email__      = '<rippmannt@ethz.ch>'


__all__ = [
    'convex_hull_numpy',
    'convex_hull_xy_numpy',
]


def convex_hull_numpy(points):
    """Compute the convex hull of a set of points.

    Parameters
    ----------
    points : list
        XYZ coordinates of the points.

    Returns
    -------
    tuple
        Indices of the points on the hull.
        Faces of the hull.

    Warning
    -------
    This function requires Numpy ands Scipy.

    Examples
    --------
    .. code-block:: python

        #

    """
    points = asarray(points)
    n, dim = points.shape

    assert 2 < dim, "The point coordinates should be at least 3D: %i" % dim

    points = points[:, :3]
    hull = ConvexHull(points)

    return hull.vertices, hull.simplices


def convex_hull_xy_numpy(points):
    """Compute the convex hull of a set of points in the XY plane.

    Warning
    -------
    This function requires Numpy ands Scipy.

    Parameters
    ----------
    points : list
        XY(Z) coordinates of the points.

    Returns
    -------
    tuple
        Indices of the points on the hull.
        Faces of the hull.

    Examples
    --------
    .. code-block:: python

        #

    """
    points = asarray(points)
    n, dim = points.shape

    assert 1 < dim, "The point coordinates should be at least 2D: %i" % dim

    points = points[:, :2]
    hull = ConvexHull(points)
    # temp = zeros((hull.vertices.shape[0], 1))
    # temp[:, :-1] = points[hull.vertices]
    # return temp
    return hull.vertices, hull.simplices


# ==============================================================================
# Main
# ==============================================================================


if __name__ == "__main__":

    # todo: distinguish between vertices of hull and internal vertices

    import random

    from compas.geometry.distance import distance_point_point

    from compas.datastructures import Mesh
    from compas.viewers import MeshViewer

    from compas.topology import mesh_unify_cycles

    radius = 5
    origin = (0., 0., 0.)
    count = 0
    points = []

    while count < 10:
        x = (random.random() - 0.5) * radius * 2
        y = (random.random() - 0.5) * radius * 2
        z = (random.random() - 0.5) * radius * 2
        pt = x, y, z

        if distance_point_point(origin, pt) <= radius:
            points.append(pt)
            count += 1

    vertices, faces = convex_hull_numpy(points)

    i_index = {i: index for index, i in enumerate(vertices)}

    mesh = Mesh.from_vertices_and_faces(
        [points[index] for index in vertices],
        [[i_index[i] for i in face] for face in faces[1:]]
    )

    mesh_unify_cycles(mesh)

    viewer = MeshViewer(mesh)

    viewer.setup()
    viewer.show()
