from compas.datastructures import Mesh
from compas.datastructures import mesh_subdivide_catmullclark
from compas.geometry import Polyhedron
from compas_viewers import SubdMeshViewer

cube = Polyhedron.generate(6)

mesh = Mesh.from_vertices_and_faces(cube.vertices, cube.faces)

viewer = SubdMeshViewer(mesh, subdfunc=mesh_subdivide_catmullclark, width=1440, height=900)

viewer.axes_on = False
viewer.grid_on = False

for _ in range(10):
    viewer.camera.zoom_in()

viewer.subdivide(k=4)

viewer.setup()
viewer.show()


# .. figure:: /_images/subdivide_mesh_catmullclark-screenshot.*
#     :figclass: figure
#     :class: figure-img img-fluid
