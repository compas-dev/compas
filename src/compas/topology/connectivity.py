from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas.itertools import pairwise


def vertex_adjacency_from_edges(edges):
    """Construct an adjacency dictionary from a set of edges.

    Parameters
    ----------
    edges : sequence[[hashable, hashable]]
        A list of node identifier pairs.

    Returns
    -------
    dict[hashable, list[hashable]]
        A dictionary mapping each node in the list of node pairs
        to a list of adjacent/connected nodes.

    Examples
    --------
    >>> edges = [[0, 1], [0, 2], [0, 3], [0, 4]]
    >>> vertex_adjacency_from_edges(edges)
    {0: [1, 2, 3, 4], 1: [0], 2: [0], 3: [0], 4: [0]}

    """
    adj = {}
    for i, j in iter(edges):
        adj.setdefault(i, []).append(j)
        adj.setdefault(j, []).append(i)
    return adj


def vertex_adjacency_from_faces(faces):
    """Construct an adjacency dictionary from a set of faces.

    Parameters
    ----------
    faces : sequence
        A sequence of faces, defined as a list of node identifiers.

    Returns
    -------
    dict
        A dictionary mapping each node in the list of node pairs
        to a list of adjacent/connected nodes.

    Examples
    --------
    >>>

    """
    adj = {}
    for face in faces:
        for u, v in pairwise(face + face[0:1]):
            adj.setdefault(u, []).append(v)
            adj.setdefault(v, []).append(u)
    return adj


def edges_from_faces(faces):
    """Construct a list of edges from a list of faces.

    Parameters
    ----------
    faces : sequence
        A sequence of faces, defined as a list of node identifiers.

    Returns
    -------
    list
        A list of edges.

    Examples
    --------
    >>>

    """
    edges = []
    seen = set()
    for face in faces:
        for u, v in pairwise(face + face[0:1]):
            if (u, v) in seen:
                continue
            if (v, u) in seen:
                continue
            seen.add((u, v))
            edges.append((u, v))
    return edges


def faces_from_edges(edges):
    """Construct a list of faces from a list of edges.

    Parameters
    ----------
    edges : sequence
        A sequence of edges, defined as a list of node identifiers.

    Returns
    -------
    list
        A list of faces.

    Examples
    --------
    >>>

    """
    faces = []
    while edges:
        u, v = edges.pop()
        face = [u, v]
        while u != v:
            for i, (x, y) in enumerate(edges):
                if v == x:
                    v = y
                    face.append(v)
                    edges.pop(i)
                    break
                if v == y:
                    v = x
                    face.append(v)
                    edges.pop(i)
                    break
        faces.append(face)
    return faces
