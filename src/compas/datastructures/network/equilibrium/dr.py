from __future__ import absolute_import
from __future__ import division
from __future__ import print_function


from compas.numerical import dr


__all__ = [
    'network_dr'
]


def network_dr(network, kmax=100, callback=None):
    """"""
    vertices = network.get_vertices_attributes(('x', 'y', 'z'))
    edges    = list(network.edges())
    fixed    = network.vertices_where({'is_fixed': True})
    loads    = network.get_vertices_attributes(('px', 'py', 'pz'), (0.0, 0.0, 0.0))
    qpre     = network.get_edges_attribute('qpre', 1.0)
    fpre     = network.get_edges_attribute('fpre', 0.0)
    lpre     = network.get_edges_attribute('lpre', 0.0)
    linit    = network.get_edges_attribute('linit', 0.0)
    E        = network.get_edges_attribute('E', 0.0)
    radius   = network.get_edges_attribute('radius', 0.0)

    xyz, q, f, l, r = dr(vertices, edges, fixed, loads, qpre, fpre, lpre, linit, E, radius,
                         kmax=kmax, callback=callback)

    for index, key in enumerate(network.vertices()):
        network.set_vertex_attributes(key, 'xyz', xyz[index])
        network.set_vertex_attributes(key, ('rx', 'ry', 'rz'), r[index])

    for index, (u, v, attr) in enumerate(network.edges(True)):
        attr['f'] = f[index]
        attr['l'] = l[index]


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':

    import random

    import compas
    from compas.datastructures import Network
    from compas.plotters import NetworkPlotter
    from compas.datastructures import network_dr
    from compas.utilities import i_to_rgb

    # make a network
    # and set the default vertex and edge attributes

    network = Network.from_obj(compas.get('lines.obj'))

    # identify the fixed vertices
    # and assign random prescribed force densities to the edges

    for key, attr in network.vertices(True):
        attr['is_fixed'] = network.vertex_degree(key) == 1

    for u, v, attr in network.edges(True):
        attr['qpre'] = 1.0 * random.randint(1, 7)

    # make a plotter for (dynamic) visualization
    # and define a callback function
    # for plotting the intermediate configurations

    plotter = NetworkPlotter(network, figsize=(10, 7), fontsize=6)

    def callback(k, xyz, crits, args):
        print(k)
        plotter.update_vertices()
        plotter.update_edges()
        plotter.update(pause=0.001)
        for key, attr in network.vertices(True):
            attr['x'] = xyz[key][0]
            attr['y'] = xyz[key][1]
            attr['z'] = xyz[key][2]

    # plot the starting configuration

    plotter.draw_vertices(facecolor={key: '#000000' for key in network.vertices_where({'is_fixed': True})})
    plotter.draw_edges()
    plotter.update(pause=1.0)

    # run the DR

    network_dr(network, callback=callback)

    # plot the final configuration

    fmax = max(network.get_edges_attribute('f'))

    plotter.draw_vertices(facecolor={key: '#000000' for key in network.vertices_where({'is_fixed': True})})
    plotter.draw_edges(color={(u, v): i_to_rgb(attr['f'] / fmax) for u, v, attr in network.edges(True)},
                       width={(u, v): 10 * attr['f'] / fmax for u, v, attr in network.edges(True)})
    plotter.show()
