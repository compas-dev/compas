from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas.topology import breadth_first_traverse
from compas.topology import connected_components


__all__ = [
    'mesh_is_connected',
    'mesh_connected_components'
]


def mesh_is_connected(mesh):
    """Verify that the mesh is connected.

    Parameters
    ----------
    mesh : compas.datastructures.Mesh
        A mesh data structure.

    Returns
    -------
    bool
        True, if the mesh is connected.
        False, otherwise.

    Notes
    -----
    A mesh is connected if for every two vertices a path exists connecting them.

    Examples
    --------
    >>> mesh_is_connected(m1)
    True
    >>> mesh_is_connected(m2)
    True
    >>> mesh_is_connected(m3)
    False
    """
    if not mesh.vertex:
        return False
    nodes = breadth_first_traverse(mesh.adjacency, mesh.get_any_vertex())
    return len(nodes) == mesh.number_of_vertices()


def mesh_connected_components(mesh):
    return connected_components(mesh.adjacency)


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    import doctest

    import compas
    from compas.datastructures import Mesh
    from compas.datastructures import meshes_join
    from compas.geometry import translate_points_xy

    m1 = Mesh.from_obj(compas.get('faces.obj'))
    m2 = m1.copy()

    points = m2.vertices_attributes('xyz')
    x, y, z = zip(*points)
    xmin = min(x)
    xmax = max(x)
    points = translate_points_xy(points, [1.5 * (xmax - xmin), 0, 0])
    for key, attr in m2.vertices(True):
        attr['x'] = points[key][0]
        attr['y'] = points[key][1]
        attr['z'] = points[key][2]

    m3 = meshes_join([m1, m2])

    doctest.testmod()
