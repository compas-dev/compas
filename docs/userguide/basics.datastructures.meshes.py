# type: ignore

# import compas
from compas.datastructures import Mesh
from compas_view2.app import App
from compas.colors import Color
from compas.geometry import Circle
from compas_view2.objects import Text

# mesh = Mesh.from_obj(compas.get("tubemesh.obj"))

# viewer = App(width=1600, height=900)
# viewer.add(mesh)
# viewer.view.camera.position = [1, -6, 1.5]
# viewer.view.camera.look_at([1, 0, 1])
# viewer.run()

# mesh = Mesh.from_meshgrid(dx=9, nx=9)

# viewer = App(viewport="top", width=1600, height=900)

# viewer.add(mesh)
# for vertex in range(30, 40):
#     color = (1.0, 0.0, 0.0) if mesh.is_vertex_on_boundary(vertex) else (0.0, 0.0, 0.0)
#     viewer.add(mesh.vertex_point(vertex), pointsize=20, pointcolor=color)

# viewer.view.camera.zoom_extents()
# viewer.view.camera.distance = 11
# viewer.run()

# mesh = Mesh.from_meshgrid(dx=9, nx=9)

# viewer = App(viewport="top", width=1600, height=900)

# red = Color.red()

# viewer.add(mesh, facecolor=(0.95, 0.95, 0.95), linewidth=2)
# viewer.add(
#     Circle.from_point_and_radius(mesh.vertex_point(23) + [0, 0, 0.1], 0.1).to_polygon(100),
#     facecolor=(1.0, 1.0, 1.0),
#     linecolor=(0.0, 0.0, 0.0),
#     linewidth=2,
# )

# for i, nbr in enumerate(mesh.vertex_neighbors(23, True)):
#     print(nbr)
#     viewer.add(
#         Circle.from_point_and_radius(mesh.vertex_point(nbr) + [0, 0, 0.1], 0.2).to_polygon(100),
#         facecolor=red.lightened(50),
#         linecolor=red,
#     )
#     viewer.add(
#         Text(
#             str(i),
#             mesh.vertex_point(nbr) + [0.09, -0.075, 0.1],
#             height=50,
#         )
#     )

# viewer.view.camera.zoom_extents()
# viewer.view.camera.distance = 11
# viewer.run()

# mesh = Mesh.from_meshgrid(dx=9, nx=9)

# viewer = App(viewport="top", width=1600, height=900)

# red = Color.red()

# viewer.add(
#     Circle.from_point_and_radius(mesh.vertex_point(23) + [0, 0, 0.1], 0.1).to_polygon(100),
#     facecolor=(1.0, 1.0, 1.0),
#     linecolor=(0.0, 0.0, 0.0),
#     linewidth=2,
# )

# facecolors = {face: (0.95, 0.95, 0.95) for face in mesh.faces()}
# for i, face in enumerate(mesh.vertex_faces(23)):
#     print(face)
#     viewer.add(
#         Text(
#             str(i),
#             mesh.face_centroid(face) + [0.09, -0.075, 0.1],
#             height=50,
#         )
#     )
#     facecolors[face] = red.lightened(50)

# viewer.add(mesh, facecolor=facecolors, linewidth=2)

# viewer.view.camera.zoom_extents()
# viewer.view.camera.distance = 11
# viewer.run()

# mesh = Mesh.from_meshgrid(dx=9, nx=9)

# viewer = App(viewport="top", width=1600, height=900)

# red = Color.red()

# viewer.add(mesh, facecolor=(0.95, 0.95, 0.95), linewidth=2)
# viewer.add(mesh.edge_line((20, 30)).translated([0, 0, 0.1]), linecolor=red, linewidth=10)

# for edge in mesh.edge_strip((20, 30)):
#     viewer.add(mesh.edge_line(edge).translated([0, 0, 0.1]), linewidth=10)

# viewer.view.camera.zoom_extents()
# viewer.view.camera.distance = 11
# viewer.run()

mesh = Mesh.from_meshgrid(dx=9, nx=9)

viewer = App(viewport="top", width=1600, height=900)

red = Color.red()

viewer.add(mesh, facecolor=(0.95, 0.95, 0.95), linewidth=2)
viewer.add(mesh.edge_line((30, 31)).translated([0, 0, 0.1]), linecolor=red, linewidth=10)

for edge in mesh.edge_loop((30, 31)):
    viewer.add(mesh.edge_line(edge).translated([0, 0, 0.1]), linewidth=10)

viewer.view.camera.zoom_extents()
viewer.view.camera.distance = 11
viewer.run()
