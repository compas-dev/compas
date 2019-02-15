from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas.topology import breadth_first_traverse


__all__ = [
    'mesh_is_connected'
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

    """
    if not mesh.vertex:
        return False

    nodes = breadth_first_traverse(mesh.adjacency, mesh.get_any_vertex())

    return len(nodes) == mesh.number_of_vertices()


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    pass
