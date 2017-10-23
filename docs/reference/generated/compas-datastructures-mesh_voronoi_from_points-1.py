from numpy import random
from numpy import hstack
from numpy import zeros

from compas.datastructures import Mesh
from compas.datastructures import trimesh_remesh
from compas.datastructures import mesh_delaunay_from_points
from compas.datastructures import mesh_voronoi_from_points

from compas.visualization import MeshPlotter

points = hstack((10.0 * random.random_sample((20, 2)), zeros((20, 1)))).tolist()
mesh = Mesh.from_vertices_and_faces(points, mesh_delaunay_from_points(points))

trimesh_remesh(mesh, 1.0, allow_boundary_split=True)

points = [mesh.vertex_coordinates(key) for key in mesh.vertices()]
voronoi, delaunay = mesh_voronoi_from_points(points, return_delaunay=True)

lines = []
for u, v in voronoi.edges():
    lines.append({
        'start': voronoi.vertex_coordinates(u, 'xy'),
        'end'  : voronoi.vertex_coordinates(v, 'xy')
    })

boundary = set(delaunay.vertices_on_boundary())

plotter = MeshPlotter(delaunay)

plotter.draw_xlines(lines)

facecolor = {key: '#0092d2' for key in delaunay.vertices() if key not in boundary}

plotter.draw_vertices(radius=0.075, facecolor=facecolor)
plotter.draw_edges(color='#cccccc')

plotter.show()