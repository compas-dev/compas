from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas.datastructures.network import Network

from compas.utilities import pairwise

__all__ = [
    'adjacency_from_edges',
    'connectivity_from_edges',
    'join_lines_to_polylines',
]


def adjacency_from_edges(edges):
    """Construct an adjacency dictionary from a set of edges.

    Parameters
    ----------
    edges : list
        A list of index pairs.

    Returns
    -------
    dict
        A dictionary mapping each index in the list of index pairs
        to a list of adjacent indices.

    Examples
    --------
    .. code-block:: python

        #

    """
    adj = {}
    for i, j in iter(edges):
        adj.setdefault(i, []).append(j)
        adj.setdefault(j, []).append(i)
    return adj


def connectivity_from_edges(edges):
    """"""
    raise NotImplementedError

def join_lines_to_polylines(lines):
    """Join polylines from lines. The polylines stop at points connecting more than two lines.

    Parameters
    ----------
    lines : list
        List of lines as tuples of their extremity coordinates.

    Returns
    -------
    polylines: list
        The polylines. If the polyline is closed, the two extremities are the same.

    """

    # create graph from line extremities
    network = Network.from_lines([(line[0], line[-1]) for line in lines])

    polylines = []
    edges_to_visit = set(network.edges())

    # initiate a polyline from an unvisited edge
    while len(edges_to_visit) > 0:
        polyline = list(edges_to_visit.pop())

        # get adjacent edges until the polyline is closed...
        while polyline[0] != polyline[-1]:

            # ... or until both end are non-two-valent vertices
            if len(network.vertex_neighbors(polyline[-1])) != 2:
                polyline = list(reversed(polyline))
                if len(network.vertex_neighbors(polyline[-1])) != 2:
                    break

            # add next edge
            polyline.append([nbr for nbr in network.vertex_neighbors(polyline[-1]) if nbr != polyline[-2]][0])

        # delete polyline edges from the list of univisted edges
        for u, v in pairwise(polyline):
            if (u, v) in edges_to_visit:
                edges_to_visit.remove((u, v))
            elif (v, u) in edges_to_visit:
                edges_to_visit.remove((v, u))

        polylines.append(polyline)

    return [[network.vertex_coordinates(vkey) for vkey in polyline] for polyline in polylines]

# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":
    pass
