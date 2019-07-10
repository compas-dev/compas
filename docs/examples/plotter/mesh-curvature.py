from numpy import array

import compas

from compas.utilities import i_to_rgb

from compas.datastructures import Mesh
from compas.datastructures import trimesh_cotangent_laplacian_matrix
from compas.datastructures import mesh_laplacian_matrix
from compas.datastructures import mesh_quads_to_triangles
from compas.datastructures import mesh_flip_cycles

from compas.geometry import add_vectors
from compas.geometry import subtract_vectors
from compas.numerical import normrow

from compas_plotters import MeshPlotter


# mesh = Mesh.from_polyhedron(8)
mesh = Mesh.from_obj(compas.get('mesh.obj'))

mesh_quads_to_triangles(mesh)
# mesh_flip_cycles(mesh)

# xyz = array(mesh.get_vertices_attributes('xyz'))

# L = mesh_laplacian_matrix(mesh)

# d = L.dot(xyz).tolist()

# curvature = normrow(d).ravel().tolist()
# print(curvature)

curvature = trimesh_gaussian_curvature(mesh)

plotter = MeshPlotter(mesh, figsize=(12, 8), tight=True)

# lines = []
# for index, key in enumerate(mesh.vertices()):
#     vector = d[index]
#     start = xyz[index]
#     end = subtract_vectors(start, vector)
#     lines.append({
#         'start' : end,
#         'end'   : start,
#         'arrow' : 'start',
#         'color' : '#ff0000'
#     })

c_min = min(curvature)
c_max = max(curvature)
c_spn = c_max - c_min

plotter.draw_vertices(
    radius=0.1,
    facecolor={key: i_to_rgb((curvature[key] - c_min) / c_spn) for key in mesh.vertices()}
)
plotter.draw_faces()

# plotter.draw_arrows(lines)

plotter.show()
