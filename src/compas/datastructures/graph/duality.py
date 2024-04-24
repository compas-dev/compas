from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from math import pi

from compas.geometry import angle_vectors
from compas.geometry import is_ccw_xy
from compas.itertools import pairwise

PI2 = 2.0 * pi


def graph_find_cycles(graph, breakpoints=None):
    """Find the faces of a graph.

    Parameters
    ----------
    graph : :class:`compas.datastructures.Graph`
        The graph object.
    breakpoints : list, optional
        The vertices at which to break the found faces.

    Notes
    -----
    Breakpoints are primarily used to break up the outside face in between
    specific vertices. For example, in structural applications involving dual
    diagrams, any vertices where external forces are applied (loads or reactions)
    should be input as breakpoints.

    Warnings
    --------
    This algorithms is essentially a wall follower (a type of maze-solving algorithm).
    It relies on the geometry of the graph to be repesented as a planar,
    straight-line embedding. It determines an ordering of the neighboring vertices
    around each vertex, and then follows the *walls* of the graph, always
    taking turns in the same direction.

    """
    if not breakpoints:
        breakpoints = []

    for u, v in graph.edges():
        graph.adjacency[u][v] = None
        graph.adjacency[v][u] = None

    graph_sort_neighbors(graph)

    leaves = list(graph.leaves())
    if leaves:
        key_xy = list(zip(leaves, graph.nodes_attributes("xy", keys=leaves)))
    else:
        key_xy = list(zip(graph.nodes(), graph.nodes_attributes("xy")))
    u = sorted(key_xy, key=lambda x: (x[1][1], x[1][0]))[0][0]

    cycles = {}
    found = {}
    ckey = 0

    v = graph_node_find_first_neighbor(graph, u)
    cycle = graph_find_edge_cycle(graph, (u, v))
    frozen = frozenset(cycle)
    found[frozen] = ckey
    cycles[ckey] = cycle
    for a, b in pairwise(cycle + cycle[:1]):
        graph.adjacency[a][b] = ckey
    ckey += 1

    for u, v in graph.edges():
        if graph.adjacency[u][v] is None:
            cycle = graph_find_edge_cycle(graph, (u, v))
            frozen = frozenset(cycle)
            if frozen not in found:
                found[frozen] = ckey
                cycles[ckey] = cycle
                ckey += 1
            for a, b in pairwise(cycle + cycle[:1]):
                graph.adjacency[a][b] = found[frozen]
        if graph.adjacency[v][u] is None:
            cycle = graph_find_edge_cycle(graph, (v, u))
            frozen = frozenset(cycle)
            if frozen not in found:
                found[frozen] = ckey
                cycles[ckey] = cycle
                ckey += 1
            for a, b in pairwise(cycle + cycle[:1]):
                graph.adjacency[a][b] = found[frozen]

    cycles = _break_cycles(cycles, breakpoints)
    return cycles


def graph_node_find_first_neighbor(graph, key):
    nbrs = graph.neighbors(key)
    if len(nbrs) == 1:
        return nbrs[0]
    ab = [-1.0, -1.0, 0.0]
    a = graph.node_coordinates(key, "xyz")
    b = [a[0] + ab[0], a[1] + ab[1], 0]
    angles = []
    for nbr in nbrs:
        c = graph.node_coordinates(nbr, "xyz")
        ac = [c[0] - a[0], c[1] - a[1], 0]
        alpha = angle_vectors(ab, ac)
        if is_ccw_xy(a, b, c, True):
            alpha = PI2 - alpha
        angles.append(alpha)
    return nbrs[angles.index(min(angles))]


def graph_sort_neighbors(graph, ccw=True):
    sorted_neighbors = {}
    xyz = {key: graph.node_coordinates(key) for key in graph.nodes()}
    for key in graph.nodes():
        nbrs = graph.neighbors(key)
        sorted_neighbors[key] = node_sort_neighbors(key, nbrs, xyz, ccw=ccw)
    for key, nbrs in sorted_neighbors.items():
        graph.node_attribute(key, "neighbors", nbrs[::-1])
    return sorted_neighbors


def node_sort_neighbors(key, nbrs, xyz, ccw=True):
    if len(nbrs) == 1:
        return nbrs
    ordered = nbrs[0:1]
    a = xyz[key]
    for i, nbr in enumerate(nbrs[1:]):
        c = xyz[nbr]
        pos = 0
        b = xyz[ordered[pos]]
        while not is_ccw_xy(a, b, c):
            pos += 1
            if pos > i:
                break
            b = xyz[ordered[pos]]
        if pos == 0:
            pos = -1
            b = xyz[ordered[pos]]
            while is_ccw_xy(a, b, c):
                pos -= 1
                if pos < -len(ordered):
                    break
                b = xyz[ordered[pos]]
            pos += 1
        ordered.insert(pos, nbr)
    if not ccw:
        return ordered[::-1]
    return ordered


def graph_find_edge_cycle(graph, edge):
    u, v = edge
    cycle = [u]
    while True:
        cycle.append(v)
        nbrs = graph.node_attribute(v, "neighbors")
        nbr = nbrs[nbrs.index(u) - 1]
        u, v = v, nbr
        if v == cycle[0]:
            break
    return cycle


def _break_cycles(cycles, breakpoints):
    breakpoints = set(breakpoints)
    broken = []

    for fkey in cycles:
        vertices = cycles[fkey]

        faces = []
        faces.append([vertices[0]])
        for i in range(1, len(vertices) - 1):
            key = vertices[i]
            faces[-1].append(key)
            if key in breakpoints:
                faces.append([key])

        faces[-1].append(vertices[-1])
        faces[-1].append(vertices[0])

        if len(faces) == 1:
            broken.append(faces[0])
            continue

        if faces[0][0] not in breakpoints and faces[-1][-1] not in breakpoints:
            if faces[0][0] == faces[-1][-1]:
                faces[:] = [faces[-1] + faces[0][1:]] + faces[1:-1]

        if len(faces) == 1:
            broken.append(faces[0])
            continue

        for vertices in faces:
            broken.append(vertices)

    return broken
