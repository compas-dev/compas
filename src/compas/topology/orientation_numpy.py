from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from scipy.spatial import cKDTree

from compas.utilities import pairwise
from compas.geometry import centroid_points
from compas.topology import breadth_first_traverse


__all__ = [
    'face_adjacency_numpy',
    'unify_cycles_numpy',
]


def unify_cycles_numpy(vertices, faces, root=0):
    """Unify the cycle directions of the given faces such that adjacent faces share opposite halfedges.

    Parameters
    ----------
    vertices : list
        A list of vertex coordinates.
    faces : list
        A list of lists of face vertex indices.
    root : int, optional
        The starting face.

    Returns
    -------
    list
        A list of faces with the same orientation as the root face.

    Raises
    ------
    AssertionError
        If not all faces were visited.

    Examples
    --------
    >>> vertices = [[0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [1.0, 1.0, 0.0], [0.0, 1.0, 1.0]]
    >>> faces = [[0, 1, 2], [0, 3, 2]]
    >>> unify_cycles(vertices, faces)
    [[0, 1, 2], [2, 3, 0]]
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
    adj = face_adjacency_numpy(vertices, faces)
    visited = breadth_first_traverse(adj, root, unify)
    assert len(list(visited)) == len(faces), 'Not all faces were visited'
    return faces


def face_adjacency_numpy(xyz, faces):
    """Construct an adjacency dictionary of the given faces, assuming that the faces have arbitrary orientation.

    Parameters
    ----------
    xyz : list
        The coordinates of the face vertices.
    faces : list
        The indices of the face vertices in the coordinates list.

    Returns
    -------
    dict
        For every face a list of neighbouring faces.

    Examples
    --------
    >>> vertices = [[0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [1.0, 1.0, 0.0], [0.0, 1.0, 1.0]]
    >>> faces = [[0, 1, 2], [0, 3, 2]]
    >>> face_adjacency(vertices, faces)
    {0: [1], 1: [0]}
    """
    f = len(faces)
    if f > 100:
        return _face_adjacency(xyz, faces)
    adjacency = {}
    for face, vertices in enumerate(faces):
        nbrs = []
        found = set()
        for u, v in pairwise(vertices + vertices[0:1]):
            for nbr, _ in enumerate(faces):
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


def _face_adjacency(xyz, faces, nmax=10, radius=2.0):
    points = [centroid_points([xyz[index] for index in face]) for face in faces]
    k = min(len(faces), nmax)
    tree = cKDTree(points)
    _, closest = tree.query(points, k=k, n_jobs=-1)
    adjacency = {}
    for face, vertices in enumerate(faces):
        nbrs = []
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


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    pass
