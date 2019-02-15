from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas

try:
    from numpy import asarray
    from scipy.spatial import ConvexHull

except ImportError:
    compas.raise_if_not_ironpython()


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

    Notes
    -----
    The faces of the hull returned by this function do not necessarily have consistent
    cycle directions. To obtain a mesh with consistent cycle directions, construct
    a mesh from the returned vertices, this function should be used in combination
    with :func:`compas.topology.unify_cycles`.

    Examples
    --------
    .. code-block:: python

        import random

        from compas.datastructures import Mesh

        from compas.geometry import distance_point_point
        from compas.geometry import convex_hull_numpy
        from compas.topology import unify_cycles

        from compas.viewers import MeshViewer

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

        vertices = [points[index] for index in vertices]
        faces = [[i_index[i] for i in face] for face in faces]
        faces = unify_cycles(vertices, faces)

        mesh = Mesh.from_vertices_and_faces(vertices, faces)

        viewer = MeshViewer(mesh)

        viewer.setup()
        viewer.show()

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
    list
        Indices of the points on the hull.
    list
        Faces of the hull.

    Notes
    -----
    The faces of the hull returned by this function do not necessarily have consistent
    cycle directions. To obtain a mesh with consistent cycle directions, construct
    a mesh from the returned vertices, this function should be used in combination
    with :func:`compas.topology.unify_cycles`.

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
    return hull.vertices, hull.simplices


# ==============================================================================
# Main
# ==============================================================================


if __name__ == "__main__":

    # todo: distinguish between vertices of hull and internal vertices

    import random

    from compas.geometry import distance_point_point

    from compas.datastructures import Mesh
    from compas.datastructures import mesh_unify_cycles
    from compas.datastructures import mesh_flip_cycles
    from compas.viewers import MeshViewer

    from compas.topology import unify_cycles

    radius = 5
    origin = (0., 0., 0.)
    count = 0
    points = []

    while count < 1000:
        x = (random.random() - 0.5) * radius * 2
        y = (random.random() - 0.5) * radius * 2
        z = (random.random() - 0.5) * radius * 2
        pt = x, y, z

        if distance_point_point(origin, pt) <= radius:
            points.append(pt)
            count += 1

    vertices, faces = convex_hull_numpy(points)

    i_index = {i: index for index, i in enumerate(vertices)}

    vertices = [points[index] for index in vertices]
    faces = [[i_index[i] for i in face] for face in faces]
    # faces = unify_cycles(vertices, faces)

    mesh = Mesh.from_vertices_and_faces(vertices, faces)

    mesh_unify_cycles(mesh)
    # mesh_flip_cycles(mesh)

    viewer = MeshViewer()

    viewer.mesh = mesh

    viewer.show()
