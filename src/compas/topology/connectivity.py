from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas.datastructures import Network

from compas.utilities import pairwise
from compas.utilities import geometric_key

__all__ = [
    'adjacency_from_edges',
    'connectivity_from_edges',
    'join_polylines',
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

def join_polylines(polylines, stops = []):
    """Join polylines. The polylines stop at points connectng more than two lines and to optional additional points.

    Parameters
    ----------
    polylines : list
        List of polylines as tuples of vertex coordinates.
    stops : list
        List of point coordinates for additional splits.

    Returns
    -------
    polylines: list
        The joined polylines. If the polyline is closed, the two extremities are the same.

    """

    # explode in lines
    lines = [(u, v) for polyline in polylines for u, v in pairwise(polyline)]
    
    # geometric keys of split points
    stop_geom_keys = set([geometric_key(xyz) for xyz in stops])

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
            if len(network.vertex_neighbors(polyline[-1])) != 2 or geometric_key(network.vertex_coordinates(polyline[-1])) in stop_geom_keys:
                polyline = list(reversed(polyline))
                if len(network.vertex_neighbors(polyline[-1])) != 2 or geometric_key(network.vertex_coordinates(polyline[-1])) in stop_geom_keys:
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
