from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas.utilities import pairwise
from compas.geometry import centroid_points
from compas.topology import breadth_first_traverse


__all__ = [
    'face_adjacency',
    'mesh_face_adjacency',
    'unify_cycles',
    'mesh_unify_cycles',
    'mesh_flip_cycles',
]


def face_adjacency(xyz, faces):
    """"""
    points = [centroid_points([xyz[index] for index in face]) for face in faces]

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
            closest = [tree.nearest_neighbors(point, 10) for point in points]
            closest = [[index for _, index, _ in nnbrs] for nnbrs in closest]

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

    for face, vertices in enumerate(faces):
        nbrs  = []
        found = set()

        nnbrs = set(closest[face])

        for u, v in pairwise(vertices + vertices[0:1]):
            for nbr in nnbrs:

                if nbr == face:
                    continue
                if nbr in found:
                    continue

                for a, b in pairwise(faces[nbr] + faces[nbr][0:1]):
                    if v == a and u == b:
                        nbrs.append(nbr)
                        found.add(nbr)
                        break

                for a, b in pairwise(faces[nbr] + faces[nbr][0:1]):
                    if u == a and v == b:
                        nbrs.append(nbr)
                        found.add(nbr)
                        break

        adjacency[face] = nbrs

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
            closest = [tree.nearest_neighbors(point, 10) for point in points]
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
                sphere = Sphere(Point3d(* point), 4.0)
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


def unify_cycles(vertices, faces, root=0):
    """"""
    def unify(node, nbr):
        # find the common edge
        for u, v in pairwise(faces[nbr] + faces[nbr][0:1]):
            if u in faces[node] and v in faces[node]:
                # node and nbr have edge u-v in common
                i = faces[node].index(u)
                j = faces[node].index(v)
                if i == j - 1 or (j == 0 and u == faces[node][-1]):
                    # if the traversal of a neighboring halfedge
                    # is in the same direction
                    # flip the neighbor
                    faces[nbr][:] = faces[nbr][::-1]
                    return

    adj = face_adjacency(vertices, faces)

    visited = breadth_first_traverse(adj, root, unify)

    assert len(list(visited)) == len(faces), 'Not all faces were visited'
    return faces


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

    from compas.datastructures.mesh import Mesh

    mesh = Mesh.from_obj(compas.get('faces_big.obj'))

    mesh_unify_cycles(mesh)
