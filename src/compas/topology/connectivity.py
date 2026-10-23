from collections.abc import Hashable
from collections.abc import Iterable
from collections.abc import Sequence
from itertools import chain
from typing import TypeVar

from compas.itertools import pairwise

Key = TypeVar("Key", bound=Hashable)


def vertex_adjacency_from_edges(edges: Iterable[tuple[Key, Key]]) -> dict[Key, list[Key]]:
    """Construct an adjacency dictionary from a set of edges.

    Parameters
    ----------
    edges
        A list of node identifier pairs.

    Returns
    -------
    dict[Key, list[Key]]
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


def vertex_adjacency_from_faces(faces: Iterable[Sequence[Key]]) -> dict[Key, list[Key]]:
    """Construct an adjacency dictionary from a set of faces.

    Parameters
    ----------
    faces
        A sequence of faces, defined as a list of node identifiers.

    Returns
    -------
    dict[Key, list[Key]]
        A dictionary mapping each node in the list of node pairs
        to a list of adjacent/connected nodes.

    """
    adj = {}
    for face in faces:
        for u, v in pairwise(chain(face, face[0:1])):
            adj.setdefault(u, []).append(v)
            adj.setdefault(v, []).append(u)
    return adj


def edges_from_faces(faces: Iterable[Sequence[Key]]) -> list[tuple[Key, Key]]:
    """Construct a list of edges from a list of faces.

    Parameters
    ----------
    faces
        A sequence of faces, defined as a list of node identifiers.

    Returns
    -------
    list[tuple[Key, Key]]
        A list of edges.

    """
    edges = []
    seen = set()
    for face in faces:
        for u, v in pairwise(chain(face, face[0:1])):
            if (u, v) in seen:
                continue
            if (v, u) in seen:
                continue
            seen.add((u, v))
            edges.append((u, v))
    return edges


def faces_from_edges(edges: list[tuple[Key, Key]]) -> list[list[Key]]:
    """Construct a list of faces from a list of edges.

    Parameters
    ----------
    edges
        A sequence of edges, defined as a list of node identifiers.

    Returns
    -------
    list[list[Key]]
        A list of faces.

    Notes
    -----
    The input list is consumed while the faces are assembled.

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
