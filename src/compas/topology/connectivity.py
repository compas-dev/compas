from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas.datastructures import Network

from compas.utilities import pairwise
from compas.utilities import geometric_key


__all__ = [
    'adjacency_from_edges',
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


# def join_lines(lines, splits = []):
#     """Join lines into polylines.
#     The polylines stop at points with a valency different from 2 in the network of line.
#     Optional splits can be included.

#     Parameters
#     ----------
#     lines : list
#         List of lines as tuples of point coordinates.
#     splits : list
#         List of point coordinates for optional splits.

#     Returns
#     -------
#     polylines: list
#         The joined polylines. If the polyline is closed, the two extremities are the same.

#     Examples
#     --------
#     Joining the lines (a, b), (b, c), (c, d), (c, e) and (e, f), where a ... f are different point coordinates will resut in the following polylines (a, b, c), (c, d) and (c, e, f).

#     .. code-block:: python

#         points = [
#             [0., 0., 0.],
#             [1., 0., 0.],
#             [2., 0., 0.],
#             [2., 1., 0.],
#             [3., 0., 0.],
#             [4., 0., 0.],
#         ]

#         lines = [
#             (points[0], points[1]),
#             (points[1], points[2]),
#             (points[2], points[3]),
#             (points[2], points[4]),
#             (points[4], points[5]),
#         ]

#         print(join_lines(lines))

#     """
#     # geometric keys of split points
#     stop_geom_keys = set([geometric_key(xyz) for xyz in splits])

#     # create graph from line extremities
#     network = Network.from_lines([(line[0], line[-1]) for line in lines])

#     polylines = []
#     edges_to_visit = set(network.edges())

#     # initiate a polyline from an unvisited edge
#     while len(edges_to_visit) > 0:
#         polyline = list(edges_to_visit.pop())

#         # get adjacent edges until the polyline is closed...
#         while polyline[0] != polyline[-1]:

#             # ... or until both end are non-two-valent vertices
#             if len(network.vertex_neighbors(polyline[-1])) != 2 or geometric_key(network.vertex_coordinates(polyline[-1])) in stop_geom_keys:
#                 polyline = list(reversed(polyline))
#                 if len(network.vertex_neighbors(polyline[-1])) != 2 or geometric_key(network.vertex_coordinates(polyline[-1])) in stop_geom_keys:
#                     break

#             # add next edge
#             polyline.append([nbr for nbr in network.vertex_neighbors(polyline[-1]) if nbr != polyline[-2]][0])

#         # delete polyline edges from the list of univisted edges
#         for u, v in pairwise(polyline):
#             if (u, v) in edges_to_visit:
#                 edges_to_visit.remove((u, v))
#             elif (v, u) in edges_to_visit:
#                 edges_to_visit.remove((v, u))

#         polylines.append(polyline)

#     return [[network.vertex_coordinates(vkey) for vkey in polyline] for polyline in polylines]


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    pass
