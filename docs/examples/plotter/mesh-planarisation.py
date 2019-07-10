import compas

from compas.datastructures import Mesh
from compas_plotters import MeshPlotter
from compas.utilities import i_to_rgb

mesh = Mesh.from_obj(compas.get('hypar.obj'))

for key, attr in mesh.vertices(True):
    attr['is_fixed'] = mesh.vertex_degree(key) == 2

fixed  = [key for key in mesh.vertices_where({'is_fixed': True})]
radius = {key: (0.05 if key in fixed else 0.01) for key in mesh.vertices()}

plotter = MeshPlotter(mesh, figsize=(10, 7))

plotter.draw_vertices(radius=radius)
plotter.draw_faces()
plotter.draw_edges()

def callback(k, args):
    print(k)

    if k % 100 == 0:
        dev = mesh_flatness(mesh, maxdev=0.02)

        plotter.update_vertices(radius=radius)
        plotter.update_faces(facecolor={fkey: i_to_rgb(dev[fkey]) for fkey in mesh.faces()})
        plotter.update_edges()
        plotter.update()

mesh_planarize_faces(mesh, fixed=fixed, kmax=2000, callback=callback)

plotter.show()
