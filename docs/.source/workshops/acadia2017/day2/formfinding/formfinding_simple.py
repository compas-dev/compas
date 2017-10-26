import compas

from compas.datastructures import Mesh
from compas.visualization import MeshPlotter
from compas.numerical import fd


__author__    = ['Tom Van Mele', ]
__copyright__ = 'Copyright 2016 - Block Research Group, ETH Zurich'
__license__   = 'MIT License'
__email__     = 'vanmelet@ethz.ch'


def main():

    # mesh and plotter

    mesh = Mesh.from_obj(compas.get('faces.obj'))
    plotter = MeshPlotter(mesh)

    # preprocess

    k_i  = mesh.key_index()

    xyz   = mesh.get_vertices_attributes('xyz')
    loads = mesh.get_vertices_attributes(('px', 'py', 'pz'), values=[0.0, 0.0, 0.0])

    fixed = [k_i[k] for k in mesh.vertices() if mesh.vertex_degree(k) == 2]
    edges = [[k_i[u], k_i[v]] for u, v in mesh.edges()]

    q = mesh.get_edges_attribute('q', 1.0)
    
    # compute equilibrium

    xyz, q, f, l, r = fd(xyz, edges, fixed, q, loads, rtype='list')

    # update

    for key, attr in mesh.vertices(True):
        x, y, z = xyz[k_i[key]]
        attr['x'] = x
        attr['y'] = y
        attr['z'] = z

    # visualize

    plotter.draw_vertices()
    plotter.draw_faces()
    plotter.draw_edges()

    plotter.show()


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":
    
    main()
