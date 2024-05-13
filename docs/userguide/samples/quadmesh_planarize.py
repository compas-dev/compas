# type: ignore
from compas_viewer import Viewer

import compas
from compas.colors import Color
from compas.colors import ColorMap
from compas.datastructures import Mesh
# ! mesh_flatness is not available in compas.geometry
from compas.datastructures import mesh_flatness
from compas.geometry import quadmesh_planarize

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

viewer = Viewer()

viewer.scene.add(mesh, facecolor=facecolor)
viewer.show()
