# type: ignore
import compas
from compas.datastructures import Mesh
from compas.datastructures import mesh_flatness
from compas.geometry import quadmesh_planarize
from compas.colors import Color, ColorMap
from compas_view2.app import App

mesh = Mesh.from_obj(compas.get("tubemesh.obj"))

V, F = mesh.to_vertices_and_faces()
V2 = quadmesh_planarize((V, F), 500, 0.005)

mesh = Mesh.from_vertices_and_faces(V2, F)
dev = mesh_flatness(mesh, maxdev=0.02)

cmap = ColorMap.from_two_colors(Color.white(), Color.blue())
facecolor = {}
for face in mesh.faces():
    if dev[face] <= 1.0:
        facecolor[face] = cmap(dev[face])
    else:
        facecolor[face] = Color.red()

viewer = App()

viewer.add(mesh, facecolor=facecolor)
viewer.run()
