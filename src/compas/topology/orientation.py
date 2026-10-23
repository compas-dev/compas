from collections.abc import Sequence

from compas._typing import CoordinateType
from compas.geometry import centroid_points
from compas.itertools import pairwise
from compas.topology.traversal import breadth_first_traverse


def _closest_faces(
    vertices: Sequence[CoordinateType],
    faces: Sequence[list[int]],
    nmax: int | None,
    max_distance: float | None,
) -> Sequence[Sequence[int]]:
    points = [centroid_points([vertices[index] for index in face]) for face in faces]

    k = len(faces) if nmax is None else min(len(faces), nmax)

    # determine the k closest faces for each face
    # each item in "closest" is
    # [0] the coordinates of the face centroid
    # [1] the index of the face in the list of face centroids
    # [2] the distance between the test point and the face centroid

    try:
        import numpy as np  # type: ignore[import-not-found]
        from scipy.spatial import cKDTree  # type: ignore[import-not-found]

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
        from compas.geometry import KDTree

        tree = KDTree(points)
        nearest = [tree.nearest_neighbors(point, k) for point in points]
        if max_distance is None:
            return [[index for _, index, _ in neighbors] for neighbors in nearest]
        return [[index for _, index, distance in neighbors if distance < max_distance] for neighbors in nearest]


def _face_adjacency(
    vertices: Sequence[CoordinateType],
    faces: Sequence[list[int]],
    nmax: int | None = None,
    max_distance: float | None = None,
) -> dict[int, list[int]]:
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


def face_adjacency(
    points: Sequence[CoordinateType],
    faces: Sequence[list[int]],
    nmax: int | None = None,
    max_distance: float | None = None,
) -> dict[int, list[int]]:
    """Build a face adjacency dict.

    Parameters
    ----------
    points
        The vertex locations of the faces.
    faces
        The faces defined as list of indices in the points list.
    nmax
        The maximum number of neighboring faces to consider. If neither nmax nor max_distance is specified, all faces will be considered.
    max_distance
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


def unify_cycles(
    vertices: Sequence[CoordinateType],
    faces: list[list[int]],
    root: int | None = None,
    nmax: int | None = None,
    max_distance: float | None = None,
) -> None:
    """Unify the cycle directions of all faces.

    Unified cycle directions is a necessary condition for the data structure to
    work properly. When in doubt, run this function on your mesh.

    Parameters
    ----------
    vertices
        The vertex coordinates of the mesh.
    faces
        The faces of the mesh defined as lists of vertex indices.
    root
        The key of the root face.
    nmax
        The maximum number of neighboring faces to consider. If neither nmax nor max_distance is specified, all faces will be considered.
    max_distance
        The max_distance of the search sphere for neighboring faces. If neither nmax nor max_distance is specified, all faces will be considered.

    Raises
    ------
    Exception
        If not all faces are included in the unification process.

    Notes
    -----
    The cycles of the faces will be aligned with the cycle direction of the root face.
    If no root face is specified, the first face in the list will be used.

    """

    def unify(node: int, nbr: int) -> None:
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
