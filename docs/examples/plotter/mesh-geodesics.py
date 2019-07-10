import compas

from compas.datastructures import Mesh
from compas.datastructures import mesh_quads_to_triangles
from compas.datastructures import mesh_flip_cycles

from compas.utilities import i_to_blue
from compas.geometry import scale_points

from compas_plotters import MeshPlotter


# mesh = Mesh.from_obj(compas.get('models/head-poses/head-reference.obj'))

mesh = Mesh.from_obj(compas.get('faces.obj'))
mesh_flip_cycles(mesh)

vertices = scale_points(mesh.get_vertices_attributes('xyz'), 10.0)

for key, attr in mesh.vertices(True):
    x, y, z = vertices[key]
    attr['x'] = x
    attr['y'] = y
    attr['z'] = z


# mesh = Mesh.from_obj(compas.get('faces.obj'))
# mesh_quads_to_triangles(mesh)

# mesh = Mesh.from_polyhedron(12)
# mesh_quads_to_triangles(mesh)

index_key = mesh.index_key()

sources = [0]

d = mesh_geodesic_distances(mesh, sources, m=1.0).tolist()

dmin = min(d)
dmax = max(d)
drange = dmax - dmin

facecolor = {key: i_to_blue(1 - (d[i] - dmin) / drange) for i, key in enumerate(mesh.vertices())}
for i in sources:
    facecolor[index_key[i]] = '#ff0000'

plotter = MeshPlotter(mesh, figsize=(6, 4))
plotter.draw_vertices(facecolor=facecolor, radius=0.5)
plotter.draw_faces()
plotter.show()
