from __future__ import print_function
from __future__ import absolute_import
from __future__ import division


__all__ = [
    'network_split_edge',
]


def network_split_edge(network, u, v, t=0.5):
    """Split and edge by inserting a vertex along its length.

    Parameters
    ----------
    u : str
        The key of the first vertex of the edge.
    v : str
        The key of the second vertex of the edge.
    t : float
        The position of the inserted vertex.

    Returns
    -------
    str
        The key of the inserted vertex.

    Raises
    ------
    ValueError
        If `t` is not `0 <= t <= 1`.
    Exception
        If `u` and `v` are not neighbors.

    Examples
    --------
    .. plot::
        :include-source:

        import compas
        from compas.datastructures import Network
        from compas.plotters import NetworkPlotter

        network = Network.from_obj(compas.get('lines.obj'))

        u, v = network.get_any_edge()

        a = network.split_edge(u, v)

        lines = []
        for u, v in network.edges():
            lines.append({
                'start': network.vertex_coordinates(u, 'xy'),
                'end'  : network.vertex_coordinates(v, 'xy'),
                'arrow': 'end',
                'width': 4.0,
                'color': '#00ff00'
            })

        plotter = NetworkPlotter(network)

        plotter.draw_lines(lines)

        plotter.draw_vertices(
            radius=0.2,
            text={key: key for key in network.vertices()},
            facecolor={key: '#ff0000' for key in (a,)}
        )
        plotter.draw_edges()

        plotter.show()

    """
    if t <= 0.0:
        raise ValueError('t should be greater than 0.0.')
    if t >= 1.0:
        raise ValueError('t should be smaller than 1.0.')

    # the split vertex
    x, y, z = network.edge_point(u, v, t)
    w = network.add_vertex(x=x, y=y, z=z)

    network.add_edge(u, w)
    network.add_edge(w, v)

    if v in network.edge[u]:
        del network.edge[u][v]
    elif u in network.edge[v]:
        del network.edge[v][u]
    else:
        raise Exception

    # split half-edge UV
    network.halfedge[u][w] = None
    network.halfedge[w][v] = None
    del network.halfedge[u][v]

    # split half-edge VU
    network.halfedge[v][w] = None
    network.halfedge[w][u] = None
    del network.halfedge[v][u]

    # return the key of the split vertex
    return w


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    import compas
    from compas.datastructures import Network
    from compas.plotters import NetworkPlotter

    network = Network.from_obj(compas.get('lines.obj'))

    a = network.split_edge(0, 22)
    b = network.split_edge(2, 30)
    c = network.split_edge(17, 21)
    d = network.split_edge(28, 16)

    lines = []
    for u, v in network.edges():
        lines.append({
            'start': network.vertex_coordinates(u, 'xy'),
            'end'  : network.vertex_coordinates(v, 'xy'),
            'arrow': 'end',
            'width': 4.0,
            'color': '#00ff00'
        })

    plotter = NetworkPlotter(network)

    plotter.draw_vertices(radius=0.2,
                          facecolor={key: '#ff0000' for key in (a, b, c, d)},
                          text={key: key for key in network.vertices()})

    plotter.draw_edges(color={(u, v): '#cccccc' for u, v in network.edges()})

    plotter.draw_lines(lines)

    plotter.show()
