import compas

from compas.datastructures import Mesh
from compas.datastructures import mesh_unweld_vertices

from compas.visualization import MeshPlotter

mesh = Mesh.from_obj(compas.get_data('faces.obj'))

fkey  = 12
where = mesh.face_vertices(fkey)[0:1]
xyz   = mesh.face_centroid(fkey)

mesh_unweld_vertices(mesh, fkey, where)

mesh.vertex[36]['x'] = xyz[0]
mesh.vertex[36]['y'] = xyz[1]
mesh.vertex[36]['z'] = xyz[2]

plotter = MeshPlotter(mesh)

plotter.draw_vertices()
plotter.draw_faces(text={fkey: fkey for fkey in mesh.faces()})

plotter.show()