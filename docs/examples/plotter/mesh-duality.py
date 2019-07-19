import compas
from compas.datastructures import Mesh
from compas.datastructures import mesh_dual
from compas_plotters import MeshPlotter

mesh = Mesh.from_obj(compas.get('faces.obj'))

dual = mesh_dual(mesh)

lines = []
for u, v in mesh.edges():
    lines.append({
        'start': mesh.vertex_coordinates(u, 'xy'),
        'end'  : mesh.vertex_coordinates(v, 'xy'),
        'color': '#cccccc',
        'width': 1.0
    })

plotter = MeshPlotter(dual)

plotter.draw_lines(lines)

plotter.draw_vertices(facecolor='#eeeeee', edgecolor='#000000', radius=0.2, text='key')
plotter.draw_edges()

plotter.show()
