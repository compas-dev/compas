from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas.topology import breadth_first_traverse
from compas.topology import connected_components


__all__ = ["mesh_is_connected", "mesh_connected_components"]


def mesh_is_connected(mesh):
    """Verify that the mesh is connected.

    Parameters
    ----------
    mesh : :class:`~compas.datastructures.Mesh`
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
    >>> from compas.datastructures import Mesh
    >>> mesh = Mesh()
    >>> mesh_is_connected(mesh)
    False
    >>> a = mesh.add_vertex(x=0, y=0, z=0)
    >>> b = mesh.add_vertex(x=1, y=0, z=0)
    >>> c = mesh.add_vertex(x=1, y=1, z=0)
    >>> mesh_is_connected(mesh)
    False
    >>> abc = mesh.add_face([a, b, c])
    >>> mesh_is_connected(mesh)
    True

    """
    if not mesh.vertex:
        return False
    nodes = breadth_first_traverse(mesh.adjacency, mesh.get_any_vertex())
    return len(nodes) == mesh.number_of_vertices()


def mesh_connected_components(mesh):
    """Find the connected components of the mesh.

    Parameters
    ----------
    mesh : :class:`~compas.datastructures.Mesh`
        A mesh data structure.

    Returns
    -------
    list[list[int]]
        Groups of connected vertices.

    """
    return connected_components(mesh.adjacency)
