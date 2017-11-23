from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas.topology import breadth_first_traverse


__author__     = 'Tom Van Mele'
__copyright__  = 'Copyright 2014, Block Research Group - ETH Zurich'
__license__    = 'MIT'
__email__      = 'vanmelet@ethz.ch'


__all__ = [
    'mesh_unify_cycles',
    'mesh_flip_cycles',
]


def face_adjacency(mesh):
    """Build a face adjacency dict.

    Parameters
    ----------
    mesh : Mesh
        A mesh object.

    Returns
    -------
    dict
        A dictionary mapping face identifiers (keys) to lists of neighbouring faces.

    Note
    ----
    This algorithm is used primarily to unify the cycle directions of a given mesh.
    Therefore, the premise is that the topological information of the mesh is corrupt
    and cannot be used to construct the adjacency structure. The algorithm is thus
    purely geometrical, but uses a spatial indexing tree to speed up the search.

    """
    fkey_index = {fkey: index for index, fkey in enumerate(mesh.faces())}
    index_fkey = {index: fkey for index, fkey in enumerate(mesh.faces())}
    points     = [mesh.face_centroid(fkey) for fkey in mesh.faces()]

    try:
        from scipy.spatial import cKDTree

        tree = cKDTree(points)
        _, closest = tree.query(points, k=10, n_jobs=-1)

    except Exception:
        try:
            import Rhino

        except Exception:
            from compas.geometry import KDTree

            tree = KDTree(points)
            closest = [tree.nearest_neighbours(point, 10) for point in points]
            closest = [[index for xyz, index, d in nnbrs] for nnbrs in closest]

        else:
            from Rhino.Geometry import RTree
            from Rhino.Geometry import Sphere
            from Rhino.Geometry import Point3d

            tree = RTree()
            for i, point in enumerate(points):
                tree.Insert(Point3d(* point), i)

            def callback(sender, e):
                data = e.Tag
                data.append(e.Id)

            closest = []
            for i, point in enumerate(points):
                sphere = Sphere(Point3d(* point), 2.0)
                data = []
                tree.Search(sphere, callback, data)
                closest.append(data)

    adjacency  = {}
    for fkey in mesh.faces():
        nbrs  = []
        index = fkey_index[fkey]
        found = set()

        nnbrs = closest[index]

        for u, v in mesh.face_halfedges(fkey):
            for index in nnbrs:
                nbr = index_fkey[index]
                if nbr == fkey:
                    continue
                if nbr in found:
                    continue
                for a, b in mesh.face_halfedges(nbr):
                    if v == a and u == b:
                        nbrs.append(nbr)
                        found.add(nbr)
                        break
                for a, b in mesh.face_halfedges(nbr):
                    if u == a and v == b:
                        nbrs.append(nbr)
                        found.add(nbr)
                        break
        adjacency[fkey] = nbrs
    return adjacency


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

    breadth_first_traverse(face_adjacency(mesh), root, unify)

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
# Main
# ==============================================================================

if __name__ == "__main__":

    import compas

    from compas.datastructures.mesh import Mesh

    mesh = Mesh.from_obj(compas.get_data('faces_big.obj'))

    mesh_unify_cycles(mesh)
