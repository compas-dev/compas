from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from math import pi

from compas.utilities import pairwise
from compas.geometry import angle_vectors
from compas.geometry import is_ccw_xy


__all__ = [
    'network_find_cycles',
]


PI2 = 2.0 * pi


def network_find_cycles(network, breakpoints=None):
    """Find the faces of a network.

    Parameters
    ----------
    network : compas.datastructures.Network
        The network object.
    breakpoints : list, optional
        The vertices at which to break the found faces.
        Default is ``None``.

    Notes
    -----
    ``breakpoints`` are primarily used to break up the outside face in between
    specific vertices. For example, in structural applications involving dual
    diagrams, any vertices where external forces are applied (loads or reactions)
    should be input as breakpoints.

    Warnings
    --------
    This algorithms is essentially a wall follower (a type of maze-solving algorithm).
    It relies on the geometry of the network to be repesented as a planar,
    straight-line embedding. It determines an ordering of the neighboring vertices
    around each vertex, and then follows the *walls* of the network, always
    taking turns in the same direction.

    Examples
    --------
    >>>

    """
    if not breakpoints:
        breakpoints = []

    for u, v in network.edges():
        network.adjacency[u][v] = None
        network.adjacency[v][u] = None

    network_sort_neighbors(network)

    leaves = list(network.leaves())
    if leaves:
        u = sorted([(key, network.node_coordinates(key, 'xy')) for key in leaves], key=lambda x: (x[1][1], x[1][0]))[0][0]
    else:
        u = sorted(network.nodes(True), key=lambda x: (x[1]['y'], x[1]['x']))[0][0]

    cycles = {}
    found = {}
    ckey = 0

    v = network_node_find_first_neighbor(network, u)
    cycle = network_find_edge_cycle(network, u, v)
    frozen = frozenset(cycle)
    found[frozen] = ckey
    cycles[ckey] = cycle
    for a, b in pairwise(cycle + cycle[:1]):
        network.adjacency[a][b] = ckey
    ckey += 1

    for u, v in network.edges():
        if network.adjacency[u][v] is None:
            cycle = network_find_edge_cycle(network, u, v)
            frozen = frozenset(cycle)
            if frozen not in found:
                found[frozen] = ckey
                cycles[ckey] = cycle
                ckey += 1
            for a, b in pairwise(cycle + cycle[:1]):
                network.adjacency[a][b] = found[frozen]
        if network.adjacency[v][u] is None:
            cycle = network_find_edge_cycle(network, v, u)
            frozen = frozenset(cycle)
            if frozen not in found:
                found[frozen] = ckey
                cycles[ckey] = cycle
                ckey += 1
            for a, b in pairwise(cycle + cycle[:1]):
                network.adjacency[a][b] = found[frozen]

    cycles = _break_cycles(cycles, breakpoints)
    return cycles


def network_node_find_first_neighbor(network, key):
    nbrs = network.neighbors(key)
    if len(nbrs) == 1:
        return nbrs[0]
    ab = [-1.0, -1.0, 0.0]
    a = network.node_coordinates(key, 'xyz')
    b = [a[0] + ab[0], a[1] + ab[1], 0]
    angles = []
    for nbr in nbrs:
        c = network.node_coordinates(nbr, 'xyz')
        ac = [c[0] - a[0], c[1] - a[1], 0]
        alpha = angle_vectors(ab, ac)
        if is_ccw_xy(a, b, c, True):
            alpha = PI2 - alpha
        angles.append(alpha)
    return nbrs[angles.index(min(angles))]


def network_sort_neighbors(network, ccw=True):
    sorted_neighbors = {}
    xyz = {key: network.node_coordinates(key) for key in network.nodes()}
    for key in network.nodes():
        nbrs = network.neighbors(key)
        sorted_neighbors[key] = node_sort_neighbors(key, nbrs, xyz, ccw=ccw)
    for key, nbrs in sorted_neighbors.items():
        network.node_attribute(key, 'neighbors', nbrs[::-1])
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


def network_find_edge_cycle(network, u, v):
    cycle = [u]
    while True:
        cycle.append(v)
        nbrs = network.node_attribute(v, 'neighbors')
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


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':

    import doctest
    doctest.testmod(globs=globals())
