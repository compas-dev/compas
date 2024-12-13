from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas.geometry import centroid_points
from compas.itertools import pairwise
from compas.topology import breadth_first_traverse


def _closest_faces(vertices, faces, nmax, max_distance):
    points = [centroid_points([vertices[index] for index in face]) for face in faces]

    k = len(faces) if nmax is None else min(len(faces), nmax)

    # determine the k closest faces for each face
    # each item in "closest" is
    # [0] the coordinates of the face centroid
    # [1] the index of the face in the list of face centroids
    # [2] the distance between the test point and the face centroid

    try:
        import numpy as np
        from scipy.spatial import cKDTree

        tree = cKDTree(points)
        distances, closest = tree.query(points, k=k, workers=-1)
        if max_distance is None:
            return closest

        closest_within_distance = []
        for i, closest_row in enumerate(closest):
            idx = np.where(distances[i] < max_distance)[0]
            closest_within_distance.append(closest_row[idx].tolist())
        return closest_within_distance

    except Exception:
        try:
            from Rhino.Geometry import Point3d  # type: ignore
            from Rhino.Geometry import RTree  # type: ignore
            from Rhino.Geometry import Sphere  # type: ignore

            tree = RTree()

            for i, point in enumerate(points):
                tree.Insert(Point3d(*point), i)

            def callback(sender, e):
                data = e.Tag
                data.append(e.Id)

            closest = []
            for i, point in enumerate(points):
                sphere = Sphere(Point3d(*point), max_distance)
                data = []
                tree.Search(sphere, callback, data)
                closest.append(data)
            return closest

        except Exception:
            from compas.geometry import KDTree

            tree = KDTree(points)
            closest = [tree.nearest_neighbors(point, k) for point in points]
            if max_distance is None:
                return closest
            return [[index for xyz, index, d in nnbrs if d < max_distance] for nnbrs in closest]


def _face_adjacency(vertices, faces, nmax=None, max_distance=None):
    if nmax is None and max_distance is None:
        raise ValueError("Either nmax or max_distance should be specified.")
    closest = _closest_faces(vertices, faces, nmax=nmax, max_distance=max_distance)

    adjacency = {}

    for index, face in enumerate(faces):
        nbrs = []
        found = set()
        nnbrs = set(closest[index])

        for u, v in pairwise(face + face[0:1]):
            for nbr in nnbrs:
                if nbr == index:
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

        adjacency[index] = nbrs

    return adjacency


def face_adjacency(points, faces, nmax=None, max_distance=None):
    """Build a face adjacency dict.

    Parameters
    ----------
    points : list[point]
        The vertex locations of the faces.
    faces : list[list[int]]
        The faces defined as list of indices in the points list.
    nmax : int, optional
        The maximum number of neighboring faces to consider. If neither nmax nor max_distance is specified, all faces will be considered.
    max_distance : float, optional
        The max_distance of the search sphere for neighboring faces. If neither nmax nor max_distance is specified, all faces will be considered.

    Returns
    -------
    dict[int, list[int]]
        A dictionary mapping face identifiers (keys) to lists of neighboring faces.

    Notes
    -----
    This algorithm is used primarily to unify the cycle directions of the faces representing a mesh.
    The premise is that the faces don't have unified cycle directions yet,
    and therefore cannot be used to construct the adjacency structure. The algorithm is thus
    purely geometrical, but uses a spatial indexing tree to speed up the search.

    """
    if nmax or max_distance:
        return _face_adjacency(points, faces, nmax=nmax, max_distance=max_distance)

    adjacency = {}

    for i, vertices in enumerate(faces):
        nbrs = []
        found = set()

        for u, v in pairwise(vertices + vertices[0:1]):
            for j, _ in enumerate(faces):
                if i == j:
                    continue
                if j in found:
                    continue

                for a, b in pairwise(faces[j] + faces[j][0:1]):
                    if v == a and u == b:
                        nbrs.append(j)
                        found.add(j)
                        break

                for a, b in pairwise(faces[j] + faces[j][0:1]):
                    if u == a and v == b:
                        nbrs.append(j)
                        found.add(j)
                        break

        adjacency[i] = nbrs

    return adjacency


def unify_cycles(vertices, faces, root=None, nmax=None, max_distance=None):
    """Unify the cycle directions of all faces.

    Unified cycle directions is a necessary condition for the data structure to
    work properly. When in doubt, run this function on your mesh.

    Parameters
    ----------
    vertices : list[[float, float, float]]
        The vertex coordinates of the mesh.
    faces : list[list[int]]
        The faces of the mesh defined as lists of vertex indices.
    root : int, optional
        The key of the root face.
    nmax : int, optional
        The maximum number of neighboring faces to consider. If neither nmax nor max_distance is specified, all faces will be considered.
    max_distance : float, optional
        The max_distance of the search sphere for neighboring faces. If neither nmax nor max_distance is specified, all faces will be considered.

    Returns
    -------
    dict
        A halfedge dictionary linking pairs of vertices to faces.

    Raises
    ------
    Exception
        If no all faces are included in the unnification process.

    Notes
    -----
    The cycles of the faces will be aligned with the cycle direction of the root face.
    If no root face is specified, the first face in the list will be used.

    """

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

    if root is None:
        # root = random.choice(list(range(len(faces))))
        root = 0

    adj = face_adjacency(vertices, faces, nmax=nmax, max_distance=max_distance)  # this is the only place where the vertex coordinates are used

    visited = breadth_first_traverse(adj, root, unify)

    if len(list(visited)) != len(faces):
        raise Exception("Not all faces were visited.")
