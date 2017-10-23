from __future__ import print_function

from compas.topology import bfs_traverse


__author__     = 'Tom Van Mele'
__copyright__  = 'Copyright 2014, Block Research Group - ETH Zurich'
__license__    = 'MIT'
__email__      = 'vanmelet@ethz.ch'


__all__ = [
    'mesh_unify_cycles',
    'mesh_flip_cycles',
]


def mesh_unify_cycles(mesh, root=None):
    """Unify the cycle directions of all faces.

    Unified cycle directions is a necessary condition for the data structure to
    work properly. When in doubt, run this function on your mesh.

    Parameters
    ----------
    mesh : Mesh
        A mesh object.
    root : str, optional [None]
        The key of the root face.

    """
    def unify(node, nbr):
        for u, v in mesh.face_halfedges(nbr):
            if u in mesh.face[node]:
                if v in mesh.face[node]:
                    i = mesh.face[node].index(u)
                    j = mesh.face[node].index(v)
                    if i == j - 1:
                        # if the traversal of a neighbouring halfedge
                        # is in the same direction
                        # flip the neighbour
                        mesh.face[nbr][:] = mesh.face[nbr][::-1]
                        return

    if root is None:
        root = mesh.get_any_face()

    bfs_traverse(mesh.face_adjacency(), root, unify)

    mesh.halfedge = {key: {} for key in mesh.vertices()}
    for fkey in mesh.faces():
        for u, v in mesh.face_halfedges(fkey):
            mesh.halfedge[u][v] = fkey
            if u not in mesh.halfedge[v]:
                mesh.halfedge[v][u] = None


def mesh_flip_cycles(mesh):
    """Flip the cycle directions of all faces.

    Parameters
    ----------
    mesh : Mesh
        A mesh object.

    Note
    ----
    This function does not care about the directions being unified or not. It
    just reverses whatever direction it finds.

    """
    mesh.halfedge = {key: {} for key in mesh.vertices()}
    for fkey in mesh.faces():
        mesh.face[fkey][:] = mesh.face[fkey][::-1]
        for u, v in mesh.face_halfedges(fkey):
            mesh.halfedge[u][v] = fkey
            if u not in mesh.halfedge[v]:
                mesh.halfedge[v][u] = None


# ==============================================================================
# Debugging
# ==============================================================================

if __name__ == "__main__":

    import compas

    from compas.datastructures.mesh import Mesh

    mesh = Mesh.from_obj(compas.get_data('faces_big.obj'))

    mesh_unify_cycles(mesh)
