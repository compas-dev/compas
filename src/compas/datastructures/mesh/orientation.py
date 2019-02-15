from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas.utilities import pairwise
from compas.geometry import centroid_points
from compas.topology import breadth_first_traverse


__all__ = [
    'mesh_face_adjacency',
    'mesh_unify_cycles',
    'mesh_flip_cycles',
]


def _mesh_face_adjacency(mesh, nmax=10, radius=2.0):
    fkey_index = {fkey: index for index, fkey in enumerate(mesh.faces())}
    index_fkey = {index: fkey for index, fkey in enumerate(mesh.faces())}
    points     = [mesh.face_centroid(fkey) for fkey in mesh.faces()]

    k = min(mesh.number_of_faces(), nmax)

    try:
        from scipy.spatial import cKDTree

        tree = cKDTree(points)
        _, closest = tree.query(points, k=k, n_jobs=-1)

    except Exception:
        try:
            import Rhino

        except Exception:
            from compas.geometry import KDTree

            tree = KDTree(points)
            closest = [tree.nearest_neighbors(point, k) for point in points]
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
                sphere = Sphere(Point3d(* point), radius)
                data = []
                tree.Search(sphere, callback, data)
                closest.append(data)

    adjacency  = {}

    for fkey in mesh.faces():
        nbrs  = []
        index = fkey_index[fkey]
        found = set()

        nnbrs = set(closest[index])

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


def mesh_face_adjacency(mesh):
    """Build a face adjacency dict.

    Parameters
    ----------
    mesh : Mesh
        A mesh object.

    Returns
    -------
    dict
        A dictionary mapping face identifiers (keys) to lists of neighboring faces.

    Notes
    -----
    This algorithm is used primarily to unify the cycle directions of a given mesh.
    Therefore, the premise is that the topological information of the mesh is corrupt
    and cannot be used to construct the adjacency structure. The algorithm is thus
    purely geometrical, but uses a spatial indexing tree to speed up the search.

    """
    f = mesh.number_of_faces()

    if f > 100:
        return _mesh_face_adjacency(mesh)

    adjacency  = {}
    faces = list(mesh.faces())

    for fkey in mesh.faces():
        # faces = []
        # for key in mesh.face_vertices(fkey):
        #     for nbr in mesh.halfedge[key]:
        #         fnbr = mesh.halfedge[key][nbr]
        #         if fnbr is not None:
        #             faces.append(fnbr)

        nbrs  = []
        found = set()

        for u, v in mesh.face_halfedges(fkey):
            for nbr in faces:
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
        # find the common edge
        for u, v in mesh.face_halfedges(nbr):
            if u in mesh.face[node] and v in mesh.face[node]:
                # node and nbr have edge u-v in common
                i = mesh.face[node].index(u)
                j = mesh.face[node].index(v)
                if i == j - 1 or (j == 0 and u == mesh.face[node][-1]):
                    # if the traversal of a neighboring halfedge
                    # is in the same direction
                    # flip the neighbor
                    mesh.face[nbr][:] = mesh.face[nbr][::-1]
                    return

    if root is None:
        root = mesh.get_any_face()

    adj = mesh_face_adjacency(mesh)

    visited = breadth_first_traverse(adj, root, unify)

    assert len(list(visited)) == mesh.number_of_faces(), 'Not all faces were visited'

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

    Notes
    -----
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

    from compas.utilities import print_profile
    from compas.datastructures import Mesh

    unify = print_profile(mesh_unify_cycles)

    mesh = Mesh.from_obj(compas.get('faces.obj'))

    unify(mesh)
