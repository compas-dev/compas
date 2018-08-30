from __future__ import print_function
from __future__ import absolute_import
from __future__ import division


__all__ = [
    'network_join_edges',
]


# def join_edges_network(network, ab, cd):
#     """Join two edges of a network.
#     """
#     intersection = set(ab) & set(cd)
#     if not intersection:
#         raise Exception('The edges are not connected.')
#     a, b = ab
#     c, d = cd
#     raise NotImplementedError


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


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":
    pass
