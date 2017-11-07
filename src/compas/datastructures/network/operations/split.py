""""""


__author__     = ['Tom Van Mele', ]
__copyright__  = 'Copyright 2014, Block Research Group - ETH Zurich'
__license__    = 'MIT License'
__email__      = 'vanmelet@ethz.ch'


__all__ = [
    'network_split_edge',
]


def network_split_edge(network, u, v, t=0.5, allow_boundary=True):
    """Split and edge by inserting a vertex along its length.

    Parameters:
        u (str): The key of the first vertex of the edge.
        v (str): The key of the second vertex of the edge.
        t (float): The position of the inserted vertex.
        allow_boundary (bool): Optional. Split boundary edges, if ``True``.
            Defaults is ``True``.

    Returns:
        str: The key of the inserted vertex.

    Raises:
        ValueError: If ``t`` is not ``0 <= t <= 1``.
        Exception: If ``u`` and ``v`` are not neighbours.


    Example:

        .. plot::
            :include-source:

            import compas
            from compas.datastructures import FaceNetwork
            from compas.plotters import FaceNetworkPlotter
            from compas.topology import network_find_faces

            network = FaceNetwork.from_obj(compas.get_data('lines.obj'))

            network_find_faces(network, breakpoints=network.leaves())

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

            plotter = FaceNetworkPlotter(network)

            plotter.draw_lines(lines)

            plotter.draw_vertices(
                radius=0.2,
                text={key: key for key in network.vertices()},
                facecolor={key: '#ff0000' for key in (a, b, c, d)}
            )
            plotter.draw_edges()
            plotter.draw_faces(
                text={fkey: fkey for fkey in network.faces()},
                facecolor={fkey: '#eeeeee' for fkey in network.faces()}
            )

            plotter.show()

    """
    if t <= 0.0:
        raise ValueError('t should be greater than 0.0.')
    if t >= 1.0:
        raise ValueError('t should be smaller than 1.0.')

    # check if the split is legal
    # don't split if edge is on boundary
    fkey_uv = network.halfedge[u][v]
    fkey_vu = network.halfedge[v][u]
    if not allow_boundary:
        if network.face:
            if fkey_uv is None or fkey_vu is None:
                return

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
    network.halfedge[u][w] = fkey_uv
    network.halfedge[w][v] = fkey_uv
    del network.halfedge[u][v]

    # update the UV face if it is not None
    if fkey_uv is not None:
        vertices = network.face[fkey_uv]
        i = vertices.index(u)
        j = vertices.index(v)
        if j > i:
            vertices.insert(j, w)
        else:
            vertices.insert(i + 1, w)
        network.face[fkey_uv][:] = vertices

    # split half-edge VU
    network.halfedge[v][w] = fkey_vu
    network.halfedge[w][u] = fkey_vu
    del network.halfedge[v][u]

    # update the VU face if it is not None
    if fkey_vu is not None:
        vertices = network.face[fkey_vu]
        i = vertices.index(v)
        j = vertices.index(u)
        if j > i:
            vertices.insert(j, w)
        else:
            vertices.insert(i + 1, w)
        network.face[fkey_vu][:] = vertices

    # return the key of the split vertex
    return w


# ==============================================================================
# Debugging
# ==============================================================================

if __name__ == "__main__":

    import compas
    from compas.datastructures import FaceNetwork
    from compas.plotters import FaceNetworkPlotter

    from compas.topology import network_find_faces

    network = FaceNetwork.from_obj(compas.get_data('lines.obj'))

    network_find_faces(network, breakpoints=network.leaves())

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

    plotter = FaceNetworkPlotter(network)

    plotter.draw_vertices(radius=0.2,
                          facecolor={key: '#ff0000' for key in (a, b, c, d)},
                          text={key: key for key in network.vertices()})

    plotter.draw_edges(color={(u, v): '#cccccc' for u, v in network.edges()})

    plotter.draw_faces(facecolor={fkey: '#eeeeee' for fkey in network.faces()},
                       text={fkey: fkey for fkey in network.faces()})

    plotter.draw_lines(lines)

    plotter.show()
