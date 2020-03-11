from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas.utilities import pairwise
from compas.utilities import geometric_key

__all__ = [
    'network_join_edges',
    'network_polylines'
]


def network_join_edges(network, key):
    nbrs = network.vertex_neighbors(key)
    if len(nbrs) != 2:
        return
    a, b = nbrs
    if a in network.edge[key]:
        del network.edge[key][a]
    else:
        del network.edge[a][key]
    del network.halfedge[key][a]
    del network.halfedge[a][key]
    if b in network.edge[key]:
        del network.edge[key][b]
    else:
        del network.edge[b][key]
    del network.halfedge[key][b]
    del network.halfedge[b][key]
    del network.vertex[key]
    del network.halfedge[key]
    del network.edge[key]
    # set attributes based on average of two joining edges?
    network.add_edge(a, b)


def network_polylines(network, splits=None):
    """Join network edges into polylines.
    The polylines stop at points with a valency different from 2 in the network of line.
    Optional splits can be included.

    Parameters
    ----------
    network : Network
        A network.
    splits : list, optional
        List of point coordinates for optional splits.
        Default is ''None''.

    Returns
    -------
    polylines: list
        The joined polylines. If the polyline is closed, the two extremities are the same.

    Examples
    --------
    Joining the lines (a, b), (b, c), (c, d), (c, e) and (e, f),
    where a ... f are different point coordinates.
    This will result in the following polylines (a, b, c), (c, d) and (c, e, f).

    >>> from compas.datastructures import Network
    >>> a = [0., 0., 0.]
    >>> b = [1., 0., 0.]
    >>> c = [2., 0., 0.]
    >>> d = [2., 1., 0.]
    >>> e = [3., 0., 0.]
    >>> f = [4., 0., 0.]
    >>> lines = [(a, b), (b, c), (c, d), (c, e), (e, f)]
    >>> network = Network.from_lines(lines)
    >>> len(network_polylines(network)) == 3
    True
    """
    # geometric keys of split points
    if splits is None:
        splits = []
    stop_geom_keys = set([geometric_key(xyz) for xyz in splits])

    polylines = []
    edges_to_visit = set(network.edges())

    # initiate a polyline from an unvisited edge
    while len(edges_to_visit) > 0:
        polyline = list(edges_to_visit.pop())

        # get adjacent edges until the polyline is closed...
        while polyline[0] != polyline[-1]:

            # ... or until both end are non-two-valent vertices
            if len(network.neighbors(polyline[-1])) != 2 or geometric_key(network.node_coordinates(polyline[-1])) in stop_geom_keys:
                polyline = list(reversed(polyline))
                if len(network.neighbors(polyline[-1])) != 2 or geometric_key(network.node_coordinates(polyline[-1])) in stop_geom_keys:
                    break

            # add next edge
            polyline.append([nbr for nbr in network.neighbors(polyline[-1]) if nbr != polyline[-2]][0])

        # delete polyline edges from the list of univisted edges
        for u, v in pairwise(polyline):
            if (u, v) in edges_to_visit:
                edges_to_visit.remove((u, v))
            elif (v, u) in edges_to_visit:
                edges_to_visit.remove((v, u))

        polylines.append(polyline)

    return [[network.node_coordinates(vkey) for vkey in polyline] for polyline in polylines]


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    import doctest
    doctest.testmod(globs=globals())
